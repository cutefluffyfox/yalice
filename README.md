# yalice
Python library for writing applications on yandex voice assistant


# Getting started
```
pip install yalice
```


This library is a wrapper for Yandex Alice, not independent library for writing web based applications, so initialization takes in an object of the type Flask
```python
from flask import Flask
from yalice import AliceBot, Message, Chat

app = Flask(__name__)
bot = AliceBot(app)
```

Your bot is going to be located on page '/post'
If you would like to change this, you can change this by adding str parameter page
```python
bot = AliceBot(app, page='/alice')
```

Also Yandex Alice can store user state and session state, pyalice give you abbility to save all that data automatically, but you can remove this abbility by adding bool parameter remember_state (to read more about states [click here](https://yandex.ru/dev/dialogs/alice/doc/session-persistence-docpage/))
```python
bot = AliceBot(app, page='/alice', remember_state=False)
```


# message handler
To hangle messages you can use decorator ```message_handler```
```python
@bot.message_handler(start_handler=True)
def start(chat: Chat, message: Message):
    chat.send_message('Hello, I am annoying Alice. I will repeat each your word!')


@bot.message_handler(tokens=['stop'], filter_func=lambda message: message.request.type == 'ButtonPressed')
def stop(chat: Chat, message: Message):
    chat.send_message('It was a fun game!')
    chat.end_session()


@bot.message_handler(unknown_handler=True)
def echo(chat: Chat, message: Message):
    chat.send_message(message.request.original_utterance)
    chat.send_button('Stop!')
```


# images
You can initialise images at the start to access easily
There is 3 ways to initialise images
```python
# 1 image at a time
bot.set_image('fox', '123456/123456')
bot.set_image('cat', '654321/654321')

# several images at a time
images = {
    'fox': '123456/123456',
    'cat': '654321/654321'
}
bot.set_images(images)

# several images at a time by using bot.images variable
bot.images = {
    'fox': '123456/123456',
    'cat': '654321/654321'
}
```

To send BigImage you can just use
```python
chat.send_image('fox')
```

But if you would like to send ItemsList
```python
chat.send_images('fox')
chat.send_images('cat')
chat.edit_images(header_text='Animals')
```


# AliceBot object
AliceBot object stores information about images, sessions states and message_handlers. Now it has methods
- ```set_image()```
- ```set_images()```
- ```message_handler()```


# Chat object
Chat object stores request to return. Now is has methods
- ```send_message()```
- ```send_button()```
- ```send_image()```
- ```send_images()```
- ```edit_images()```
- ```end_session()```
- ```set_session_state()```
- ```set_user_state()```

# Message object
Message object is parsed json, to see json structure [click here](https://yandex.ru/dev/dialogs/alice/doc/protocol-docpage/)

# Links
Telegram [@cutefluffyfox](https://t.me/cutefluffyfox)<br>
VK [@cutefluffyfox](https://vk.com/cutefluffyfox)<br>
Expired by [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
