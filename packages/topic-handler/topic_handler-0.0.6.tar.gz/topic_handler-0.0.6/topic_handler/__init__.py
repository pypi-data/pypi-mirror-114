
from .Global import RequestFormat, ResponseError
from kafka import KafkaProducer
import re
from cryptography.hazmat.primitives.serialization.base import (
    load_pem_public_key,
)
import jwt


class Aux:
    required_permissions = []

    def initi_data():
        pass

    def send_response():
        pass


def names_to_snake_case(data):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', data.__class__.__name__).lower()


class Messages:
    def __init__(self, topic, value, offset, partition):
        self.topic = topic
        self.value = value
        self.offset = offset
        self.partition = partition


class Event:
    def __init__(self, message: Messages):
        self.message = message


class RequestData:
    auth_id: str
    response_topic: str

    def __init__(self, auth_id, response_topic):
        self.auth_id = auth_id
        self.response_topic = response_topic


class HandlerTopics():
    is_error = False

    def __init__(self, topic_list: list, HOST_KAFKA, PUBLIC_KEY_JWT):
        self.exist_topics = list(map(lambda x: x(), topic_list))
        self.topics_names = list(map(names_to_snake_case, self.exist_topics))
        self.HOST_KAFKA = HOST_KAFKA
        self.PUBLIC_KEY_JWT = PUBLIC_KEY_JWT

    def get_instances(self):
        return self.topics_names

    def select_topic(self, topic):
        select: list[Aux] = list(
            filter(lambda x: names_to_snake_case(x) == topic, self.exist_topics))
        if select.__len__() == 0 or select.__len__() > 1:
            self.is_error = True
            return
        self.selected_topic = select[0]

    def response(self, event: Event):
        self.create_response_topic(event.message)
        if self.is_error:
            return
        try:
            data = RequestFormat().FromString(event.message.value)
            self.token = data.token
            self.selected_topic.initi_data(
                data.language, data.token, self.response_topic, event.message.value)
        except:
            self.response_on_error(ResponseError(
                res=400, msg="bad request").SerializeToString())
            return
        if self.selected_topic.required_permissions:
            self.decode_jwt(self.selected_topic.required_permissions)

        if self.is_error:
            self.response_on_error(ResponseError(
                res=400, msg=self.msg).SerializeToString())
            return
        self.selected_topic.send_response()

    def create_response_topic(self, message: Messages):
        self.response_topic = (
            message.topic
            + "_"
            + str(message.offset)
            + "_"
            + str(message.partition)
        )

    def response_on_error(self, response_model: bytes):
        producer = KafkaProducer(bootstrap_servers=self.HOST_KAFKA)
        producer.send(self.response_topic, response_model)
        producer.flush(timeout=10)

    def decode_jwt(self, required_permissions):
        pub_rsakey = load_pem_public_key(self.PUBLIC_KEY_JWT)
        try:
            options = {"require": ["uid", "aud", "iat"]}
            payload = jwt.decode(
                self.token,
                pub_rsakey,
                audience=required_permissions,
                algorithms=["RS256"],
                options=options,
            )
            self.auth_id = payload['uid']
        except jwt.ExpiredSignatureError:
            self.is_error = True
            self.msg = "EXPIRED_TOKEN"
        except jwt.InvalidAudience:
            self.is_error = True
            self.msg = "NOT_AUTHORIZED"
        except Exception as e:
            self.is_error = True
            self.msg = str(e)
