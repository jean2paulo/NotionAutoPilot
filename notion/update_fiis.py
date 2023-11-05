import os
import gspread
import logging
from notion.commons import utils as notion_utils

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
spreadsheet_id = '1rKgwERiE6CQhK69sBun9N2dsGegAHTWctPS_KiHVM_8'
worksheet_name = 'FUNDAMENTUS_FIIS'  # Nome da planilha
sh = googleClient.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

# Percorrer todas as linhas da planilha
data = worksheet.get_all_records(numericise_ignore=['all'])
count_success = 0
for row in data:
    try:

        # page id
        notion_page_id = notion_utils.format_page_id(row['ID'])
    
        # name
        name = row['NAME']

        # segmento
        stringSegment = row['SEGMENTO']
        if stringSegment != "#N/A":
            notion_utils.notion_update(
                notion,
                notion_page_id,
                notion_utils.notion_update_string('Segmento', stringSegment)
            )

        # price
        stringPrice = row['PRICE']
        if stringPrice != "#N/A":
            price = float(stringPrice.replace(",", "."))
            notion_utils.notion_update(
                notion,
                notion_page_id,
                notion_utils.notion_update_number('Price', price)
            )

        # VP Cota
        stringVPCota = row['VP_COTA']
        if stringVPCota != "#N/A":
            vpCota = float(stringVPCota.replace(",", "."))
            notion_utils.notion_update(
                notion,
                notion_page_id,
                notion_utils.notion_update_number('VP_COTA', vpCota)
            )
        
        # PVP
        stringPVP = row['PVP']
        if stringPVP != "#N/A":
            pvp = float(stringPVP.replace(",", "."))
            notion_utils.notion_update(
                notion,
                notion_page_id,
                notion_utils.notion_update_number('PVP', pvp)
            )

        # DY
        stringDy = row['DY']
        if stringDy != "#N/A":
            dy = float(stringDy.replace(",", ".").replace('%', ''))/100
            notion_utils.notion_update(
                notion,
                notion_page_id,
                notion_utils.notion_update_number('DY', dy)
            )

        print(f'Updating {name}.. ')
    except Exception as e:
        print(f"[update_fundamentus_fiis] ERROR: {e}")
        #logger.error(f"[update_fundamentus_fiis] ERROR: {e.with_traceback}")
