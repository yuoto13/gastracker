import asyncio
import requests
from web3 import Web3
from telebot import TeleBot
import aiohttp
import config  # Импортируем файл конфигурации

# Подключение к Ethereum
web3 = Web3(Web3.HTTPProvider(endpoint_uri=config.ETH_ENDPOINT_URI))

# URL для подключения к StarkNet
STARKNET_URL = config.STARKNET_URL

bot = TeleBot(config.TELEGRAM_TOKEN)

# Функция для получения цены газа на Ethereum
def get_gas_price_eth():
    return round(web3.eth.gas_price / 10**9, 2)

# Асинхронная функция для получения цены газа на StarkNet
async def get_gas_price_starknet():
    async with aiohttp.ClientSession() as session:
        async with session.post(STARKNET_URL, json={
            "jsonrpc": "2.0",
            "method": "starknet_blockNumber",
            "params": [],
            "id": 1
        }) as response:
            if response.status == 200:
                block = await response.json()
                if "result" in block:
                    block_number = block["result"]
                else:
                    print("Error: 'result' not in block response", block)
                    return None

                # Теперь получаем информацию о блоке
                async with session.post(STARKNET_URL, json={
                    "jsonrpc": "2.0",
                    "method": "starknet_getBlockWithTxHashes",
                    "params": [{"block_number": block_number}],
                    "id": 2
                }) as block_response:
                    if block_response.status == 200:
                        block_data = await block_response.json()
                        if "result" in block_data:
                            if "l1_gas_price" in block_data["result"] and "price_in_wei" in block_data["result"]["l1_gas_price"]:
                                return round(int(block_data["result"]["l1_gas_price"]["price_in_wei"], 16) / 10**9, 2)
                            else:
                                print("Error: 'l1_gas_price' or 'price_in_wei' not in block_data result", block_data)
                                return None
                        else:
                            print("Error: 'result' not in block_data response", block_data)
                            return None
                    else:
                        print("Error: Block response status code", block_response.status)
                        return None
            else:
                print("Error: Initial response status code", response.status)
                return None

# Функция для отправки сообщения в Telegram
def send_message(message):
    bot.send_message(chat_id=config.CHAT_ID, text=message)

# Основная функция, запускающая цикл обновления
async def main():
    while True:
        # Получение актуальной цены газа на Ethereum
        eth_gas_price = get_gas_price_eth()

        # Получение актуальной цены газа на StarkNet
        stark_gas_price = await get_gas_price_starknet()

        # Определение эмодзи для цены газа на Ethereum
        if eth_gas_price <= 15:
            eth_emoji = "🟩"
        elif 15 < eth_gas_price <= 25:
            eth_emoji = "🟧"
        else:
            eth_emoji = "🟥"

        # Определение эмодзи для цены газа на StarkNet
        if stark_gas_price is not None:
            if stark_gas_price <= 15:
                stark_emoji = "🟩"
            elif 15 < stark_gas_price <= 25:
                stark_emoji = "🟧"
            else:
                stark_emoji = "🟥"
        else:
            stark_emoji = "❓"
            stark_gas_price = "N/A"

        # Формирование сообщения
        message = f"{eth_emoji} {eth_gas_price} | {stark_emoji} {stark_gas_price}\nETH | STARKNET"

        # Отправка сообщения в Telegram
        send_message(message)

        # Задержка 10 секунд
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
