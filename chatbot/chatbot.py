import os
import telebot

from utils import get_daily_horoscope

# CONSTANTS
WHATSAPP_BOT_TERM = "whatsapp"

#init

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(telegram_bot_token)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

def buildWhatsappLink(number, text):
  textEncoded = urllib.parse.quote(text)
  url = f"Link: https://wa.me/{number}/?text={textEncoded}"
  return url

@bot.message_handler(commands=[WHATSAPP_BOT_TERM])
def send_wa_link(message):
    parameter = string.replace(f'/{WHATSAPP_BOT_TERM}', '')
    string_parameters = parameter.strip().split(maxsplit=1)
    url = buildWhatsappLink(string_parameters[0], string_parameters[1])
    bot.reply_to(message, url)

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)


def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())


def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
