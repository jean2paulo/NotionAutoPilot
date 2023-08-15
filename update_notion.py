import gspread
from notion.client import NotionClient
import os
import base64

# Ler as variáveis de ambiente
credentials_base64 = os.getenv('GOOGLE_SHEET_CREDENTIALS_JSON')
credentials_json = base64.b64decode(credentials_base64).decode("utf-8")
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente do Google Sheets e Notion
gc = gspread.service_account_from_dict(credentials_json)
client = NotionClient(token_v2=notion_token)

# ID da planilha do Google Sheets
spreadsheet_id = '1rKgwERiE6CQhK69sBun9N2dsGegAHTWctPS_KiHVM_8'
worksheet_name = 'QUOTES'  # Nome da planilha
sh = gc.open_by_key(spreadsheet_id)
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
