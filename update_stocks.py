import os
import gspread
import logging
import notion.financial.stocks as notion_stocks
import third_party.fundamentus.details as fundamentus

from notion_client import Client
from oauth2client.service_account import ServiceAccountCredentials

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente de Notion
notion = Client(auth=notion_token)

# Percorrer todas as linhas da tabela no notion
data = notion_stocks.get_fundamentus_stocks_id(notion)

count_success = 0
for stock in data:
    try:
        # init local properties
        name = stock['name']
        id = stock['id']
        properties = {}

        # get details from fundamentus
        df = fundamentus.get_detalhes_papel(name)

         # Sector
        try:
            sector = df.Setor.values[0]
            properties['setor'] = sector
        except Exception as e:
            logger.error(f'[update_stocks_v2][setor][{name}]: {e}')


        # Cotacao
        try:
            cotacao = int(df.Cotacao.values[0])/100
            properties['cotacao'] = cotacao
        except Exception as e:
            logger.error(f'[update_stocks_v2][update_cotacao][{name}] : {e}')

        # PVP
        try:
            pvp = int(df.PVP.values[0]) / 100
            properties['pvp'] = pvp
        except Exception as e:
            logger.error(f'[update_fiis_v2][update_pvp][{name}] : {e}')

        # PL
        try:
            pl = int(df.PL.values[0]) / 100
            properties['pl'] = pl
        except Exception as e:
            logger.error(f'[update_stocks_v2][update_pl][{name}] : {e}')

        # DY
        try:
            dy = float(df.Div_Yield.values[0].replace(",", ".").replace('%', '')) / 100
            properties['dy'] = dy
        except Exception as e:
            logger.error(f'[update_stocks_v2][update_dy][{name}] : {e}')

      
        # Update properties in notion
        notion_stocks.update_fundamentus_stocks(notion, id, properties)
        
        count_success += 1
    except Exception as e:
        logger.error(f'[update_stocks_v2][get_fundamentus][{name}] : {e}')

print(str(count_success) + '/' + str(len(data)))