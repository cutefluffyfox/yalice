class Interfaces:
    def __init__(self, interface: dict):
        self.screen = interface['screen']
        self.account_linking = interface['account_linking']


class MetaData:
    def __init__(self, meta: dict):
        self.locale = meta['locale']
        self.timezone = meta['timezone']
        self.interfaces = Interfaces(interface=meta['interfaces'])


class User:
    def __init__(self, user: dict):
        self.user_id = user['user_id']
        self.access_token = user.get('access_token')


class Application:
    def __init__(self, application: dict):
        self.application_id = application['application_id']


class SessionData:
    def __init__(self, session: dict):
        self.session_id = session['session_id']
        self.message_id = session['message_id']
        self.skill_id = session['skill_id']
        self.user = User(user=session['user'])
        self.application = Application(application=session['application'])
        self.new = session['new']


class Markup:
    def __init__(self, markup: dict):
        self.dangerous_context = markup['dangerous_context']


class Entity:
    def __init__(self, entity: dict):
        self.start = entity['tokens']['start']
        self.end = entity['tokens']['end']
        self.type = entity['type']
        self.value = entity['value']


class Entities:
    def __init__(self, entities: list):
        self.datetime = None
        self.fio = None
        self.geo = None
        self.number = None
        for entity in entities:
            if entity['type'] == 'YANDEX.DATETIME':
                self.datetime = Entity(entity=entity)
            elif entity['type'] == 'YANDEX.FIO':
                self.fio = Entity(entity=entity)
            elif entity['type'] == 'YANDEX.GEO':
                self.geo = Entity(entity=entity)
            elif entity['type'] == 'YANDEX.NUMBER':
                self.number = Entity(entity=entity)


class NLU:
    def __init__(self, nlu: dict):
        self.tokens = nlu['tokens']
        self.entities = Entities(entities=nlu['entities'])


class RequestData:
    def __init__(self, request_json: dict):
        self.command = request_json['command']
        self.original_utterance = request_json['original_utterance']
        self.type = request_json['type']
        self.markup = Markup(markup=request_json['markup'])
        self.payload = request_json.get('payload')
        self.nlu = NLU(nlu=request_json['nlu'])


class StateValue:
    def __init__(self, session: dict):
        self.value = session.get('value') if session.get('value') is not None else None


class State:
    def __init__(self, state: dict):
        self.session = StateValue(session=state.get('session'))
        self.user = StateValue(session=state.get('user'))


class Message:
    def __init__(self, json: dict):
        self.meta = MetaData(json['meta'])
        self.session = SessionData(json['session'])
        self.version = json['version']
        self.request = RequestData(request_json=json['request'])
        self.state = State(state=json.get('state'))
        self.original_request = json
