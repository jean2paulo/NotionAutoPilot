from notion.commons import utils as notion_utils
from .constants import *
from .strings import *

def get_fundamentus_stocks_id(notion):
    data = _get_fundamentus_stocks(notion)
    fundamentus_stocks = []
    if (len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            id = notion_utils.extract_id(result)
            name = notion_utils.extract_title(result, STOCK_NAME_NOTION_PROPERTY)
            fundamentus_stocks.append({
                'id': id,
                'name': name,
            })

    return fundamentus_stocks

def update_fundamentus_stocks(notion, page_id, properties):
    notion_utils.notion_update(
        notion,
        page_id,
        properties={
            **notion_utils.notion_update_string(STOCK_SECTOR_NOTION_PROPERTY, properties['setor']),
            **notion_utils.notion_update_number(STOCK_PRICE_NOTION_PROPERTY, properties['cotacao']),
            **notion_utils.notion_update_number(STOCK_PL_NOTION_PROPERTY, properties['pl']), 
            **notion_utils.notion_update_number(STOCK_PVP_NOTION_PROPERTY, properties['pvp']), 
            **notion_utils.notion_update_number(STOCK_DY_NOTION_PROPERTY, properties['dy'])  
        }
    )

# Private Methods

def _get_fundamentus_stocks(notion):
    return notion_utils.notion_query(
        notion, STOCKS_PAGE_ID,
    )