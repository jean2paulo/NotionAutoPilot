import os
import gspread
from notion_client import Client
from oauth2client.service_account import ServiceAccountCredentials

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
worksheet_name = 'QUOTES'  # Nome da planilha
sh = googleClient.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

# Percorrer todas as linhas da planilha
data = worksheet.get_all_records(numericise_ignore=['all'])
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

            print(f"✓ {name}: {price}")
        else:
            print(f"✖ {name}: #N/A")
            
    except Exception as e:
        print("Ocorreu um erro: ", e)
