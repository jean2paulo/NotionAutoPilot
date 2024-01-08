from notion.commons import utils as notion_utils
from .constants import *
from .strings import *

def get_fundamentus_stocks_id(notion):
    data = _get_fundamentus_stocks(notion)
    fundamentus_stocks = []
    if (len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            id = notion_utils.extract_id(result)
            name = notion_utils.extract_title(result, FUNDAMENTUS_STOCK_NAME_NOTION_PROPERTY)
            fundamentus_stocks.append({
                'id': id,
                'name': name,
            })

    return fundamentus_stocks

def get_top_stocks(notion):
    data = _get_report_stocks_top(notion)
    message = '📊 Top Açoes\n'

    if (len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            name = notion_utils.extract_title(result, REPORT_STOCK_NAME_NOTION_PROPERTY)
            dy = notion_utils.extract_formula_number(result, REPORT_STOCK_DY_NOTION_PROPERTY)
            pvp = notion_utils.extract_formula_number(result, REPORT_STOCK_PVP_NOTION_PROPERTY)
            price = notion_utils.extract_formula_number(result, REPORT_STOCK_PRICE_NOTION_PROPERTY)

            dy = notion_utils.formatar_percentage(dy)
            price = notion_utils.format_real(price)
            
            message += f"[{dy}] {name} -> (pvp: {pvp}\tprice: {price})\n"

    return message

def update_fundamentus_stocks(notion, page_id, properties):
    notion_utils.notion_update(
        notion,
        page_id,
        properties={
            **notion_utils.notion_update_string(FUNDAMENTUS_STOCK_SECTOR_NOTION_PROPERTY, properties['setor']),
            **notion_utils.notion_update_number(FUNDAMENTUS_STOCK_PRICE_NOTION_PROPERTY, properties['cotacao']),
            **notion_utils.notion_update_number(FUNDAMENTUS_STOCK_PL_NOTION_PROPERTY, properties['pl']), 
            **notion_utils.notion_update_number(FUNDAMENTUS_STOCK_PVP_NOTION_PROPERTY, properties['pvp']), 
            **notion_utils.notion_update_number(FUNDAMENTUS_STOCK_DY_NOTION_PROPERTY, properties['dy'])  
        }
    )

# Private Methods

def _get_fundamentus_stocks(notion):
    return notion_utils.notion_query(
        notion, FUNDAMENTUS_STOCKS_PAGE_ID,
    )

def _get_report_stocks_top(notion):
    return notion_utils.notion_query(
        notion, REPORT_STOCKS_PAGE_ID,
        filter= notion_utils.notion_filter_number(
            REPORT_STOCK_DY_NOTION_PROPERTY, 0.08, notion_utils.FILTER_GREATER_THAN_OR_EQUAL_TO
        ),
        sort=[ notion_utils.notion_sort_desc(REPORT_STOCK_DY_NOTION_PROPERTY) ],
        page_size=15
    )