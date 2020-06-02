from flask import Flask, request
from json import dumps
from alice_types import Message


class AliceBot:
    def __init__(self, app: Flask, page='/post', remember_state=True):
        self.app = app
        self.remember_state = remember_state
        self.last_states = {}
        self.message_handlers = []
        self.images = {}
        self.unknown_handler = lambda chat, message: None
        self.__create_page(page=page)

    def __create_page(self, page='/post'):
        @self.app.route(page, methods=['POST'])
        def post_alice():
            message = Message(request.json)
            chat = Chat(self, message)

            for func in self.message_handlers:
                if not chat:
                    func(chat, message)
            if not chat:
                self.unknown_handler(chat, message)

            return dumps(chat.get_response())

    def message_handler(self, start_handler=False, unknown_handler=False, filter_func=lambda message: True):
        def decorator(func):
            def wrapped(chat: Chat, message: Message, *args, **kwargs):
                if filter_func(message) and message.session.new == start_handler:
                    func(chat, message, *args, **kwargs)
            if unknown_handler:
                self.unknown_handler = wrapped
            else:
                self.message_handlers.append(wrapped)
        return decorator

    def set_images(self, images: dict):
        self.images = images

    def set_image(self, name: str, image: str):
        self.images[name] = image


class Chat:
    def __init__(self, bot: AliceBot, message: Message):
        self.bot = bot
        self.session_id = message.session.session_id
        self.user_id = message.session.user.user_id
        self.response = {
            'response': {
                'text': '',
                'buttons': [],
                'card': {},
                'end_session': False
            },
            'session_state': {
                'value': None
            },
            'user_state_update': {
                'value': None
            },
            'version': message.version
        }
        if self.bot.last_states.get(self.session_id) is None:
            self.bot.last_states[self.session_id] = message.state.session.value
        if self.bot.last_states.get(self.user_id) is None:
            self.bot.last_states[self.user_id] = message.state.user.value

    def get_response(self) -> dict:
        if not self.response['response']['card']:
            del self.response['response']['card']
        if self.bot.remember_state and self.response['session_state']['value'] is None:
            self.response['session_state']['value'] = self.bot.last_states.get(self.session_id)
        if self.bot.remember_state and self.response['user_state_update']['value'] is None:
            self.response['user_state_update']['value'] = self.bot.last_states.get(self.user_id)

        return self.response

    def send_message(self, text: str, tts=None):
        self.response['response']['text'] = text
        self.response['response']['tts'] = tts

    def send_button(self, title: str, hide=True, url=None, payload=None):
        self.response['response']['buttons'].append({'title': title, 'hide': hide, 'url': url, 'payload': payload})

    def send_image(self, image: str, title=None, description=None, button_text=None, button_url=None, button_payload=None):
        self.response['response']['card'] = {
            'type': 'BigImage',
            'title': title,
            'description': description,
            'image_id': self.bot.images.get(image) if self.bot.images.get(image) else image,
            'button': {
                'text': button_text,
                'url': button_url,
                'payload': button_payload
            }
        }

    def send_images(self, image: str, title=None, description=None, button_text=None, button_url=None, button_payload=None):
        self.response['response']['card']['type'] = 'ItemsList'
        self.response['response']['card']['items'] = self.response['response']['card'].get('items', [])
        self.response['response']['card']['items'].append({
            'title': title,
            'description': description,
            'image_id': self.bot.images.get(image) if self.bot.images.get(image) else image,
            'button': {
                'text': button_text,
                'url': button_url,
                'payload': button_payload
            }
        })

    def edit_images(self, header_text=None, footer_text=None, button_text=None, button_url=None, button_payload=None):
        if header_text is not None:
            self.response['response']['card']['header'] = {'text': header_text}
        if footer_text is not None:
            self.response['response']['card']['footer'] = {
                'text': footer_text,
                'button': {
                    'text': button_text,
                    'url': button_url,
                    'payload': button_payload
                }
            }

    def end_session(self, end=True):
        self.response['response']['end_session'] = end

    def set_session_state(self, value):
        """https://yandex.ru/dev/dialogs/alice/doc/session-persistence-docpage/"""
        if self.bot.remember_state:
            self.bot.last_states[self.session_id] = value
        self.response['session_state']['value'] = value

    def set_user_state(self, value):
        if self.bot.remember_state:
            self.bot.last_states[self.user_id] = value
        self.response['user_state_update']['value'] = value

    def __bool__(self):
        return bool(
            self.response['response']['text'] or
            self.response['response']['buttons'] or
            self.response['response']['card']
        )
