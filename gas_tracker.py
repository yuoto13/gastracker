from web3 import Web3
from telebot import TeleBot
import time

# Подключение к Ethereum
web3 = Web3(Web3.HTTPProvider(endpoint_uri='https://rpc.notadegen.com/eth'))

# Подключение к Telegram
TOKEN = "6675870031:AAHEsCASQsVq9_OA98EPmdYO7e3y9ggoDts"
bot = TeleBot(TOKEN)

# Функция для получения цены газа
def get_gas_price():
    return round(web3.eth.gas_price / 10**9, 2)

# Функция для отправки сообщения в Telegram
def send_message(message):
    bot.send_message(chat_id="-1001885026748", text=message)

# Цикл для обновления цены газа каждые 10 секунд
while True:
    # Получение актуальной цены газа
    gas_price = get_gas_price()

    # Отправка сообщения в Telegram
    send_message(f"🟥 {gas_price}")

    # Задержка 10 секунд
    time.sleep(10)

