import os
import gspread
import logging

from notion_client import Client
from oauth2client.service_account import ServiceAccountCredentials

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
credentials_file = os.getenv('GOOGLE_CLOUD_CREDENTIALS_FILE')
notion_token = os.getenv('NOTION_TOKEN')

# Defina o escopo e carregue as credenciais do arquivo JSON
scope = [
    "https://www.googleapis.com/auth/drive", 
    "https://www.googleapis.com/auth/spreadsheets"
]

# credentials = service_account.Credentials.from_service_account_file(credentials_file) # Using oauth2client
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

# Configurar cliente do Google Sheets
googleClient = gspread.authorize(credentials)

# Configurar cliente de Notion
notion = Client(auth=notion_token)

# ID da planilha do Google Sheets
spreadsheet_id = '1khFog2fFvQ63Tj2mJyUG2rWkU2IvSThbzTFvsJuU9eo'
worksheet_name = 'QUOTES'  # Nome da planilha
sh = googleClient.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

# Percorrer todas as linhas da planilha
data = worksheet.get_all_records(numericise_ignore=['all'])
count_success = 0
for row in data:
    try:
    
        notion_page_id = row['ID']
        formatted_page_id = f"{notion_page_id[:8]}-{notion_page_id[8:12]}-{notion_page_id[12:16]}-{notion_page_id[16:20]}-{notion_page_id[20:]}"
    
        name = row['NAME']
        stringPrice = row['PRICE']
        
        if stringPrice != "#N/A":
            price = float(stringPrice.replace(",", "."))
    
            # Atualizar o valor na propriedade "Price" da página no Notion
            notion.pages.update(
                formatted_page_id,
                properties={"Price":{"number": price}},
            )
            count_success += 1
            
    except Exception as e:
        logger.error(f"[update_quotes] ERROR: {e.with_traceback}")

print(f"{count_success}/{len(data)}")
