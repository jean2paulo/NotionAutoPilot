import os
import logging

from notion_client import Client
from notion.tasks import read_tasks

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente de Notion
notion = Client(auth=notion_token)

tasks_message = read_tasks.check_all_tasks(notion)

full_message = f"{tasks_message}\n"

print(full_message)