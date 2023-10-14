#from utils import create_task
from notion.tasks import utils as task_utils

# Bot terms
NOTION_TASK_CREATE_BOT_TERM = "notion_task_create"

def init(notion, message, bot):
    text = message.text
    parameters = text.replace(f'/{NOTION_TASK_CREATE_BOT_TERM}', '')
    string_parameters = parameters.strip().split(maxsplit=1)

    if(len(string_parameters) > 0):
        notion.pages.create(
            task_utils.create_task(
                string_parameters[0]
            )
        )

    bot.reply_to(message, "Nova atividade criada!")
