import os
import telebot
from notion.tasks import utils
from notion.tasks import create_tasks
from notion.tasks import read_tasks
from notion.birthday import today_birthday
from notion import my_calendar
from notion.commitment import today_commitment
from notion.financial import month as financial_month

from notion_client import Client

from telegram import whatsapp
from telegram import horoscope 

#init

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(telegram_bot_token)

@bot.message_handler(commands=['id'])
def send_welcome(message):
    bot.reply_to(message, message.chat.id)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=[whatsapp.WHATSAPP_BOT_TERM])
def send_wa_link(message):
    whatsapp.whatsapp_flow(message, bot)

@bot.message_handler(commands=[horoscope.HOROSCOPE_BOT_TERM])
def send_horoscope(message):
    horoscope.horoscope_flow(message, bot)

# NOTION

# Ler as variáveis de ambiente
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente de Notion
notion = Client(auth=notion_token)

# tasks

@bot.message_handler(commands=[create_tasks.NOTION_TASK_CREATE_BOT_TERM])
def create_task(message):
    create_tasks.init(notion, message, bot)

@bot.message_handler(commands=[read_tasks.NOTION_CHECK_TASKS_BOT_TERM])
def check_tasks(message):
    read_tasks.check_tasks(notion, message, bot)

@bot.message_handler(commands=["notion_check_all_tasks"])
def check_tasks(message):
    full_message = read_tasks.check_all_tasks(notion)
    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )

# birthday

@bot.message_handler(commands=["notion_check_today_birthday"])
def check_today_birthday(message):
    full_message = today_birthday.check_today_birthday(notion)
    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )

# calendario

@bot.message_handler(commands=["notion_check_today_calendar"])
def check_today_calendar(message):
    full_message = my_calendar.check_today_calendar(notion)
    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )

# financial month

@bot.message_handler(commands=["notion_check_financial_month_total"])
def check_financial_month_totals(message):
    full_message = financial_month.check_financial_month_totals(notion)
    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )


# commitment

@bot.message_handler(commands=["notion_check_today_commitment"])
def check_today_commitment(message):
    full_message = today_commitment.check_today_commitment(notion)
    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )

# morning report
@bot.message_handler(commands=["morning_report"])
def morning_report(message):
    birthday_message = today_birthday.check_today_birthday(notion)
    calendar_message = my_calendar.check_today_calendar(notion)
    commitment_message = today_commitment.check_today_commitment(notion)
    tasks_message = read_tasks.check_all_tasks(notion)
    financial_message = financial_month.check_financial_month_totals(notion)

    full_message = "Bom dia Jean! ☀️\nEsse eh o seu reporte para o dia de hoje:\n\n"
    full_message += f"{financial_message}\n\n"
    full_message += f"{birthday_message}\n\n"
    full_message += f"{calendar_message}\n\n"
    full_message += f"{commitment_message}\n\n"
    full_message += f"{tasks_message}\n"

    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )

# mirror

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(f"Respondendo mensagem -> {message}")
    bot.reply_to(message, message.text)

bot.infinity_polling()
