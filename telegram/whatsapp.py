import urllib

WHATSAPP_BOT_TERM = "whatsapp"

def whatsapp_flow(message, bot):
    text = message.text
    parameters = text.replace(f'/{WHATSAPP_BOT_TERM}', '')
    string_parameters = parameters.strip().split(maxsplit=1)
    if(len(string_parameters) == 0):
        sent_msg = bot.send_message(message.chat.id, "Numero do telefone?", parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, phone_number_handler, bot)
    else:
        url = build_whatsapp_link(string_parameters[0], string_parameters[1])
        bot.reply_to(message, url)

def phone_number_handler(message, bot):
    phone_number = message.text
    text = "Mensagem: "
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, message_handler, bot, phone_number)
    
def message_handler(message, bot, phone_number):
    text = message.text
    url = build_whatsapp_link(phone_number, text)
    print("BOT: Gerando whatsapp url...")
    bot.send_message(message.chat.id, url, parse_mode="Markdown")
    
def build_whatsapp_link(phone_number, text):
    textEncoded = urllib.parse.quote(text)
    url = f"Link: https://wa.me/{phone_number}/?text={textEncoded}"
    return url
