import os
import logging
import telebot

from notion_client import Client
from notion.my_calendar import today_calendar
from notion.birthday import today_birthday
from notion.commitment import today_commitment
from notion.financial import month
from notion.tasks import all_tasks
from third_party import advice_slip

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

# Welcome message
advice = f"\n_💭 {advice_slip.get_random_quote()}_\n"
welcome_message = f"Bom dia *Jean!* ☀️\n{advice}\nEsse é o seu reporte para o dia de hoje:"

# Morning Routine
bot.send_message(
    telegram_bot_id, 
    welcome_message,
    parse_mode="Markdown"
)

# Birthday
bot.send_message(
    telegram_bot_id, 
    today_birthday.get_today_birthday_message(notion),
    parse_mode="Markdown"
)

# Calendar
bot.send_message(
    telegram_bot_id, 
    today_calendar.get_today_calendar_message(notion),
    parse_mode="Markdown"
)

# Commitment
bot.send_message(
    telegram_bot_id, 
    today_commitment.get_today_commitment_message(notion),
    parse_mode="Markdown"
)

# Financial
bot.send_message(
    telegram_bot_id, 
    month.get_totals_message(notion),
    parse_mode="Markdown"
)

# Tasks
bot.send_message(
    telegram_bot_id, 
    all_tasks.get_all_tasks_message(notion),
    parse_mode="Markdown"
)