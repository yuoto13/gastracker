import asyncio
import aiohttp
from web3 import Web3
from telebot import TeleBot
import config
import time

bot = TeleBot(config.TELEGRAM_TOKEN)

networks = {
    "ETH": {
        "url": config.ETH_ENDPOINT_URI,
        "web3": Web3(Web3.HTTPProvider(config.ETH_ENDPOINT_URI))
    },
    "BLAST": {
        "url": config.BLAST_URL,
        "web3": Web3(Web3.HTTPProvider(config.BLAST_URL))
    },
    "SCROLL": {
        "url": config.SCROLL_URL,
        "web3": Web3(Web3.HTTPProvider(config.SCROLL_URL))
    },
    "LINEA": {
        "url": config.LINEA_URL,
        "web3": Web3(Web3.HTTPProvider(config.LINEA_URL))
    },
    "BASE": {
        "url": config.BASE_URL,
        "web3": Web3(Web3.HTTPProvider(config.BASE_URL))
    },
    "STARKNET": {
        "url": config.STARKNET_URL,
        "web3": None
    }
}

last_sent_time = time.time()

def get_gas_price_eth(network_name):
    if network_name != "STARKNET":
        return round(networks[network_name]["web3"].eth.gas_price / 10**9, 3)
    return None

async def get_gas_price_starknet():
    async with aiohttp.ClientSession() as session:
        async with session.post(config.STARKNET_URL, json={
            "jsonrpc": "2.0",
            "method": "starknet_blockNumber",
            "params": [],
            "id": 1
        }) as response:
            if response.status == 200:
                block = await response.json()
                block_number = block.get("result")
                if block_number:
                    async with session.post(config.STARKNET_URL, json={
                        "jsonrpc": "2.0",
                        "method": "starknet_getBlockWithTxHashes",
                        "params": [{"block_number": block_number}],
                        "id": 2
                    }) as block_response:
                        if block_response.status == 200:
                            block_data = await block_response.json()
                            if "result" in block_data and "l1_gas_price" in block_data["result"]:
                                return round(int(block_data["result"]["l1_gas_price"]["price_in_wei"], 16) / 10**9, 3)
                        return None
            return None

def send_message(message, photo=None):
    if photo:
        with open(photo, 'rb') as photo_file:
            bot.send_photo(chat_id=config.CHAT_ID, photo=photo_file, caption=message, parse_mode='HTML')
    else:
        bot.send_message(chat_id=config.CHAT_ID, text=message, parse_mode='HTML')

async def main():
    global last_sent_time

    while True:
        current_time = time.time()
        messages = []
        updated_prices = {}

        for network_name in networks:
            if network_name != "STARKNET":
                eth_gas_price = get_gas_price_eth(network_name)

                if eth_gas_price <= 15:
                    eth_emoji = "🟢"
                elif 15 < eth_gas_price <= 25:
                    eth_emoji = "🟠"
                else:
                    eth_emoji = "🔴"

                messages.append(f"{eth_emoji} <b>{eth_gas_price}</b> - <b>{network_name}</b>")
                updated_prices[network_name] = eth_gas_price

            else:
                stark_gas_price = await get_gas_price_starknet()

                if stark_gas_price is not None:
                    if stark_gas_price <= 15:
                        stark_emoji = "🟢"
                    elif 15 < stark_gas_price <= 25:
                        stark_emoji = "🟠"
                    else:
                        stark_emoji = "🔴"
                else:
                    stark_emoji = "❓"
                    stark_gas_price = "N/A"

                messages.append(f"{stark_emoji} <b>{stark_gas_price}</b> - <b>StarkNet</b>")
                updated_prices["StarkNet"] = stark_gas_price

        if current_time - last_sent_time >= 60:
            final_message = "\n".join(messages)
            footer_message = "\n\nProd by @devheadb"

            photo_path = "static/bot1.jpg"

            send_message(final_message + footer_message, photo=photo_path)

            last_sent_time = current_time

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())