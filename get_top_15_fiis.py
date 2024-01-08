import os
import logging
import telebot

from notion.financial import fiis
from notion_client import Client

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
notion_token = os.getenv('NOTION_TOKEN')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_bot_id = os.getenv('TELEGRAM_BOT_ID')

# Configurar cliente de Notion
notion = Client(auth=notion_token)
bot = telebot.TeleBot(telegram_bot_token)

# Percorrer todas as linhas da tabela no notion
top_fiis_message = fiis.get_top_fiis(notion)

try:
    # send top fiis 
    bot.send_message(
        telegram_bot_id, 
        top_fiis_message,
        parse_mode="Markdown"
    )
except Exception as e:
    logger.error(f"[get_top_15_fiis] : {e}")