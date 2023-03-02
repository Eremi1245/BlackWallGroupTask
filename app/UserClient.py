import json
from multiprocessing import Process
import sys
import threading
import time
import pika
import uuid
from Worker import worker


class UserClient(object):
    """
    Класс создает соединение, отправляет запрос и ждет ответ
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        user_queue = self.channel.queue_declare(queue='', exclusive=True)
        self.user_queue = str(uuid.uuid4())

        callback_queue = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = callback_queue.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            body = json.loads(body)
            self.response = body

    def send(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.user_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=body)
        self.connection.process_data_events(time_limit=None)
        print(self.response)

    def get_balance(self):
        body = {
            "user_id": self.user_id,
            "operation": "get_balance"
        }

        json_string = json.dumps(body)

        self.send(json_string)

    def add_money(self, money: int):
        body = {
            "user_id": self.user_id,
            "operation": "add_money",
            "money": money
        }

        json_string = json.dumps(body)

        self.send(json_string)

    def buy_for_money(self, cost: int):
        body = {
            "user_id": self.user_id,
            "operation": "buy_for_money",
            "cost": cost
        }

        json_string = json.dumps(body)

        self.send(json_string)
