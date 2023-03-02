import json
import time
import pika
import requests


def worker(user_queue):
    """
    Функция создает воркер запросов юзера, отправляет запрос на сервер и получает ответ от сервера
    и возвращает его юзеру
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    channel.queue_declare(queue=user_queue)

    def fib(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    def on_request(ch, method, props, body: str):
        body = json.loads(body)
        operation = body.get("operation")
        user_id = body.get("user_id")
        if operation == "get_balance":
            result = requests.get(
                f"http://127.0.0.1:8000/clients/{user_id}")
        elif operation == "add_money":
            money = body.get('money')
            result = requests.put(
                f"http://127.0.0.1:8000/clients/add/{user_id}?value={money}")
        elif operation == "buy_for_money":
            cost = body.get('cost')
            result = requests.put(
                f"http://127.0.0.1:8000/clients/buy/{user_id}?value={cost}")

        response = {
            "status": result.status_code,
            "body": result.json()
        }

        response_str = json.dumps(response)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=response_str)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # устанавливаем прослушку очереди
    channel.basic_consume(queue=user_queue, on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
