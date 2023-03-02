import threading
import time
from UserClient import UserClient
from Worker import worker


def client():
    """
    1) Функция создает клиента
    2) Функция создает поток с отдельной очередью RabbitMQ, которая хранит запросы клиента
    3) Поток отключается вместе с выходом из функции
    """
    user = UserClient(1)
    time.sleep(1)
    new_thread = threading.Thread(
        target=worker, args=(user.user_queue,)
    )
    new_thread.daemon = True
    new_thread.start()
    time.sleep(1)
    print("Exit for exit")
    while True:
        x = input("выберите действие: "
                  "\n 1 - Узнать баланс"
                  "\n 2 - Пополнить баланс"
                  "\n 3 - Купить"
                  "\n")
        if x == "exit":
            break
        elif x == '1':
            user.get_balance()
        elif x == '2':
            money = input("Введите сумму пополнения: ")
            user.add_money(int(money))
        elif x == '3':
            money = input("Введите сумму покупки: ")
            user.buy_for_money(int(money))


if __name__ == '__main__':
    client()
