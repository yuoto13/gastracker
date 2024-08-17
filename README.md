# Gas Price Monitor Bot

Этот бот отслеживает цены на газ в Ethereum и StarkNet и отправляет обновления в Telegram.

## Настройка

### Шаг 1: Клонирование репозитория

Клонируйте репозиторий:

```sh
git clone https://your-repo-url.git
cd your-repo-directory
```

### Шаг 2: Создание конфигурационного файла

Создайте файл `config.py` на основе `config_temp.py` и заполните его своими данными:

```sh
cp config_temp.py config.py
```

Отредактируйте `config.py`, добавив свои данные:

```python
# config.py

ETH_ENDPOINT_URI = 'https://your_eth_endpoint_here'
STARKNET_URL = "https://your_starknet_url_here"
TELEGRAM_TOKEN = "your_telegram_token_here"
CHAT_ID = "your_chat_id_here"
```

### Шаг 3: Установка зависимостей

Установите зависимости из файла `requirements.txt`:

```sh
pip install -r requirements.txt
```

### Шаг 4: Запуск бота

Запустите бота:

```sh
python main.py
```

## Зависимости

Для работы бота необходимы следующие зависимости:

- `web3`: для работы с Ethereum.
- `pyTelegramBotAPI`: для взаимодействия с Telegram.
- `aiohttp`: для выполнения асинхронных HTTP-запросов.

Все зависимости указаны в файле `requirements.txt` и могут быть установлены с помощью команды:

```sh
pip install -r requirements.txt
```
