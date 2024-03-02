from web3 import Web3
from telebot import TeleBot
import time

# Подключение к Ethereum
web3 = Web3(Web3.HTTPProvider(endpoint_uri='https://binance.llamarpc.com'))

# Подключение к Telegram
TOKEN = "AAHZBC22fv7LSPImG0YxhrgC90aKNBUBXrc"
bot = TeleBot(TOKEN)

# Функция для получения цены газа
def get_gas_price():
    return round(web3.eth.gas_price / 10**9, 2)

# Функция для отправки сообщения в Telegram
def send_message(message):
    bot.send_message(chat_id= "-1002074638970", text=message)

# Цикл для обновления цены газа каждые 10 секунд
while True:
    # Получение актуальной цены газа
    gas_price = get_gas_price()

    # Отправка сообщения в Telegram
    send_message(f"Цена газа:  🟥 {gas_price}")

    # Задержка 10 секунд
    time.sleep(10)

