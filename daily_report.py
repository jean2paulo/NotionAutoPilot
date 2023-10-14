import os
import logging

from notion_client import Client
from notion.tasks import read_tasks
from notion import birthday
from notion import calendar
from notion import commitment
from notion import financial_month

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente de Notion
notion = Client(auth=notion_token)

birthday_message = birthday.check_today_birthday(notion)
calendar_message = calendar.check_today_calendar(notion)
commitment_message = commitment.check_today_commitment(notion)
tasks_message = read_tasks.check_all_tasks(notion)
financial_message = financial_month.check_financial_month_totals(notion)

full_message = "Bom dia Jean! ☀️ \nEsse eh o seu reporte para o dia de hoje:\n\n"
full_message += f"{financial_message}\n\n"
full_message += f"{birthday_message}\n\n"
full_message += f"{calendar_message}\n\n"
full_message += f"{commitment_message}\n\n"
full_message += f"{tasks_message}\n"

with open("daily_report_output.txt", "w") as file:
    file.write(full_message)