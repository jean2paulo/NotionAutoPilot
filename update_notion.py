import os
import gspread
from notion_client import Client
from google.oauth2 import service_account

# Ler as variáveis de ambiente
credentials_file = os.getenv('GOOGLE_CLOUD_CREDENTIALS_FILE')
notion_token = os.getenv('NOTION_TOKEN')

# Defina o escopo e carregue as credenciais do arquivo JSON
scope = [
    "https://www.googleapis.com/auth/drive", 
    "https://www.googleapis.com/auth/spreadsheets"
]
credentials = service_account.Credentials.from_json_keyfile_name(credentials_file, scope)

# Configurar cliente do Google Sheets
googleClient = gspread.authorize(credentials)

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
