import os
import logging
import notion.financial.fiis as notion_fiis
import third_party.fundamentus.details as fundamentus

from notion_client import Client

# Configurando o nível de log
logging.basicConfig(filename='log_error.txt', level=logging.INFO)

# Criando um logger
logger = logging.getLogger()

# Ler as variáveis de ambiente
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente de Notion
notion = Client(auth=notion_token)

# Percorrer todas as linhas da tabela no notion
data = notion_fiis.get_fundamentus_fiis_id(notion)

count_success = 0
for fii in data:
    try:
        # init local properties
        name = fii['name']
        id = fii['id']
        properties = {}

        # get details from fundamentus
        df = fundamentus.get_detalhes_papel(name)

        # Segmento
        try:
            segmento = df.Segmento.values[0]
            properties['segmento'] = segmento
        except Exception as e:
            logger.error(f'[update_fiis_v2][update_segmento][{name}]: {e}')


        # Cotacao
        try:
            cotacao = int(df.Cotacao.values[0])/100
            properties['cotacao'] = cotacao
        except Exception as e:
            logger.error(f'[update_fiis_v2][update_cotacao][{name}] : {e}')

        # VP COTA
        try:
            vp_cota = int(df.VPCota.values[0]) / 100
            properties['vp_cota'] = vp_cota
        except Exception as e:
            logger.error(f'[update_fiis_v2][update_vp_cota][{name}] : {e}')

        # PVP
        try:
            pvp = int(df.PVP.values[0]) / 100
            properties['pvp'] = pvp
        except Exception as e:
            logger.error(f'[update_fiis_v2][update_pvp][{name}] : {e}')

        # DY
        try:
            dy = float(df.Div_Yield.values[0].replace(",", ".").replace('%', '')) / 100
            properties['dy'] = dy
        except Exception as e:
            logger.error(f'[update_fiis_v2][update_dy][{name}] : {e}')

        # Update properties in notion
        notion_fiis.update_fundamentus_fiis(notion, id, properties)
        
        count_success += 1
    except Exception as e:
        logger.error(f'[update_fiis_v2][get_fundamentus][{name}] : {e}')


print(str(count_success) + '/' + str(len(data)))