from web3 import Web3
from telebot import TeleBot
import time

# Подключение 
web3 = Web3(Web3.HTTPProvider(endpoint_uri='https://rpc.notadegen.com/eth'))

web3_stark = Web3(Web3.HTTPProvider(endpoint_uri='https://rpc.starknet.io'))

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
    # Получение актуальной цены газа на Ethereum
    eth_gas_price = get_gas_price()

    # Получение актуальной цены газа на StarkNet
    stark_gas_price = get_stark_gas_price()

    # Определение эмодзи для цены газа на Ethereum
    if eth_gas_price <= 15:
        eth_emoji = "🟩"
    elif 15 < eth_gas_price <= 25:
        eth_emoji = "🟧"
    else:
        eth_emoji = "🟥"

    # Определение эмодзи для цены газа на StarkNet
    if stark_gas_price <= 15:
        stark_emoji = "🟩"
    elif 15 < stark_gas_price <= 25:
        stark_emoji = "🟧"
    else:
        stark_emoji = "🟥"

    # Формирование сообщения
    message = f"{eth_emoji} {eth_gas_price} | {stark_emoji} {stark_gas_price}\nETH | STARKNET"

    # Отправка сообщения в Telegram
    send_message(message)

    # Задержка 10 секунд
    time.sleep(10)
