import os
import gspread
import logging
import time
import details

from oauth2client.service_account import ServiceAccountCredentials

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
credentials_file = os.getenv('GOOGLE_CLOUD_CREDENTIALS_FILE')

# Defina o escopo e carregue as credenciais do arquivo JSON
scope = [
    "https://www.googleapis.com/auth/drive", 
    "https://www.googleapis.com/auth/spreadsheets"
]

# credentials = service_account.Credentials.from_service_account_file(credentials_file) # Using oauth2client
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

# Configurar cliente do Google Sheets
googleClient = gspread.authorize(credentials)

# ID da planilha do Google Sheets
spreadsheet_id = '1rKgwERiE6CQhK69sBun9N2dsGegAHTWctPS_KiHVM_8'
worksheet_name = 'FUNDAMENTUS_FIIS'  # Nome da planilha

# Definindo os indexes das colunas 
COTACAO_COLUMN = 3
SEGMENTO_COLUMN = 4
VPCOTA_COLUMN = 5
PVP_COLUMN = 6
DY_COLUMN = 7

sh = googleClient.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

# Percorrer todas as linhas da planilha
data = worksheet.get_all_records(numericise_ignore=['all'])

for index, row in enumerate(data, start=2):
    name = row['NAME']
    
    try:

        # Fundamentus 
        df = details.get_detalhes_papel(name)

        # Cotacao
        try:
            cotacao = int(df.Cotacao.values[0])/100
            worksheet.update_cell(index, COTACAO_COLUMN, cotacao)
        except Exception as e:
            print(f'[ERRO - Cotacao] {name} : {e}')

        # Segmento
        try:
            segmento = df.Segmento.values[0]
            worksheet.update_cell(index, SEGMENTO_COLUMN, segmento)
        except Exception as e:
            print(f'[ERRO - Segmento] {name} : {e}')

        
        # VP COTA
        try:
            vp_cota = int(df.VPCota.values[0]) / 100
            worksheet.update_cell(index, VPCOTA_COLUMN, vp_cota)
        except Exception as e:
            print(f'[ERRO - VP Cota] {name} : {e}')

        # PVP
        try:
            pvp = int(df.PVP.values[0]) / 100
            worksheet.update_cell(index, PVP_COLUMN, pvp)
        except Exception as e:
            print(f'[ERRO - PVP] {name} : {e}')

        # DY
        try:
            dy = df.Div_Yield.values[0].replace('.', ',')
            worksheet.update_cell(index, DY_COLUMN, dy)        
        except Exception as e:
            print(f'[ERRO - DY] {name} : {e}')
        
    except Exception as e:
        print(f'[ERRO] {name} : {e}')
        
    time.sleep(10)