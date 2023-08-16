import os
import gspread
from notion_client import Client
import json
import base64
from google.oauth2 import service_account

# Ler as variáveis de ambiente
credentials_base64 = os.getenv('GOOGLE_SHEET_CREDENTIALS_JSON')
credentials_json = base64.b64decode(credentials_base64).decode("utf-8")

notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente do Google Sheets
credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))
googleClient = gs.authorize(credentials)

# Configurar cliente de Notion
client = Client(auth=notion_token)

# ID da planilha do Google Sheets
spreadsheet_id = '1rKgwERiE6CQhK69sBun9N2dsGegAHTWctPS_KiHVM_8'
worksheet_name = 'QUOTES'  # Nome da planilha
sh = googleClient.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

# Percorrer todas as linhas da planilha
data = worksheet.get_all_records()
for row in data:
    notion_page_url = row['URL']
    new_value = row['PRICE']

    # Pegar a página Notion correspondente
    notion_page = client.get_block(notion_page_url)

    # Atualizar o valor na propriedade "Price" da página no Notion
    notion_property = notion_page.collection.get_schema_property('Price')
    notion_page.set_property(notion_property['id'], new_value)
