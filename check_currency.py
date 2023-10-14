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
spreadsheet_id = '1QljCc1VfhLL2yTvskJh3dErChu_37rBXNPz2VqzppAw'
worksheet_name = 'MAX_MIN'  # Nome da planilha
sh = googleClient.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

def get_cell_number(row, column): return float(worksheet.cell(row, column).value.replace(",", "."))

def format_brl(number): return "R$ {valor:,.2f}".format(valor=abs(number))
def format_clp(number): return "$ {valor:,.0f}".format(valor=abs(number))
def format_usd(number): return "$ {valor:,.2f}".format(valor=abs(number))

def check_max(worksheet, currency_column):
    act = get_cell_number(2, currency_column)

    if(act > get_cell_number(13, currency_column)):
        return '{🔥 Max. 60 dias}'
    elif(act > get_cell_number(12, currency_column)):
        return '{💥 Max. 45 dias}' 
    elif(act > get_cell_number(11, currency_column)):
        return '{🔴 Max. 30 dias}'
    elif(act > get_cell_number(10, currency_column)):
        return '{❗ Max. 15 dias}'
    elif(act > get_cell_number(9, currency_column)):
        return '{❕ Max. 7 dias}'
    else:
        return None

def check_min(worksheet, currency_column):
    act = get_cell_number(2, currency_column)

    if(act < get_cell_number(8, currency_column)):
        return '{🔥 Min. 60 dias}'
    elif(act < get_cell_number(7, currency_column)):
        return '{💥 Min. 45 dias}' 
    elif(act < get_cell_number(6, currency_column)):
        return '{🔴 Min. 30 dias}'
    elif(act < get_cell_number(5, currency_column)):
        return '{❗ Min. 15 dias}'
    elif(act < get_cell_number(4, currency_column)):
        return '{❕ Min. 7 dias}'
    else:
        return None

#🇺🇸 → 🇨🇱 → 🇧🇷
full_message = '💱 Cotaçao\n'

# USDCLP
usdclp_column = 3
usdclp_act = get_cell_number(2, usdclp_column)
usdclp_yesterday = get_cell_number(3, usdclp_column)

if(usdclp_act > usdclp_yesterday):
    sinal = "↗️"
else:
    sinal = "↘️"

full_message += f"\n🇺🇸🇨🇱 → {format_clp(usdclp_act)}{sinal}"

if(check_max(usdclp_act, usdclp_column) != None):
    full_message += f" {check_max(usdclp_act, usdclp_column)}"
elif(check_min(usdclp_act, usdclp_column) != None):
    full_message += f" {check_min(usdclp_act, usdclp_column)}"
else:
    full_message += ""

# BRLCLP
brlclp_column = 4
brlclp_act = get_cell_number(2, brlclp_column)
brlclp_yesterday = get_cell_number(3, brlclp_column)

if(brlclp_act > brlclp_yesterday):
    sinal = "↗️"
else:
    sinal = "↘️"

full_message += f"\n🇧🇷🇨🇱 → {format_clp(brlclp_act)}{sinal}"

if(check_max(brlclp_act, brlclp_column) != None):
    full_message += f" {check_max(brlclp_act, brlclp_column)}"
elif(check_min(brlclp_act, brlclp_column) != None):
    full_message += f" {check_min(brlclp_act, brlclp_column)}"
else:
    full_message += ""

# USDBRL
usdbrl_column = 5
usdbrl_act = get_cell_number(2, usdbrl_column)
usdbrl_yesterday = get_cell_number(3, usdbrl_column)

if(usdbrl_act > usdbrl_yesterday):
    sinal = "↗️"
else:
    sinal = "↘️"

full_message += f"\n🇺🇸🇧🇷 → {format_brl(usdbrl_act)}{sinal}"

if(check_max(usdbrl_act, brlclp_column) != None):
    full_message += f" {check_max(usdbrl_act, brlclp_column)}"
elif(check_min(usdbrl_act, brlclp_column) != None):
    full_message += f" {check_max(usdbrl_act, brlclp_column)}"
else:
    full_message += ""

print(full_message)