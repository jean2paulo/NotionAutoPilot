from notion.commons import utils as notion_utils
from .constants import *
from .strings import *

def get_fundamentus_fiis_id(notion):
    data = notion_utils.notion_query(
        notion, FUNDAMENTUS_FIIS_PAGE_ID,
    )
    fundamentus_fiis = []
    if (len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            id = notion_utils.extract_id(result)
            name = notion_utils.extract_title(result, FUNDAMENTUS_FII_NAME_NOTION_PROPERTY)
            fundamentus_fiis.append({
                'id': id,
                'name': name,
            })

    return fundamentus_fiis

def get_top_fiis(notion):
    data = _get_report_fiis_top(notion)
    message = '🏢 Top Fundos Imobilarios\n'

    if (len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            name = notion_utils.extract_title(result, REPORT_FII_NAME_NOTION_PROPERTY)
            dy = notion_utils.extract_formula_number(result, REPORT_FII_DY_NOTION_PROPERTY)
            pvp = notion_utils.extract_formula_number(result, REPORT_FII_PVP_NOTION_PROPERTY)
            price = notion_utils.extract_formula_number(result, REPORT_FII_PRICE_NOTION_PROPERTY)

            dy = notion_utils.formatar_percentage(dy)
            price = notion_utils.format_real(price)
            
            message += f"[{dy}] {name} -> (pvp: {pvp}\tprice: {price})\n"

    return message

def update_fundamentus_fiis(notion, page_id, properties):
    notion_utils.notion_update(
        notion,
        page_id,
        properties={
            **notion_utils.notion_update_string(FUNDAMENTUS_FII_SEGMENT_NOTION_PROPERTY, properties['segmento']),
            **notion_utils.notion_update_number(FUNDAMENTUS_FII_PRICE_NOTION_PROPERTY, properties['cotacao']),
            **notion_utils.notion_update_number(FUNDAMENTUS_FII_VP_COTA_NOTION_PROPERTY, properties['vp_cota']), 
            **notion_utils.notion_update_number(FUNDAMENTUS_FII_PVP_NOTION_PROPERTY, properties['pvp']), 
            **notion_utils.notion_update_number(FUNDAMENTUS_FII_DY_NOTION_PROPERTY, properties['dy'])  
        }
    )

# private methods
    
def _get_report_fiis_top(notion):
    return notion_utils.notion_query(
        notion, REPORT_FIIS_PAGE_ID,
        filter= notion_utils.notion_filter_and(
            notion_utils.notion_filter_number(
                REPORT_FII_DY_NOTION_PROPERTY, 0.12, notion_utils.FILTER_GREATER_THAN_OR_EQUAL_TO
            ),
            notion_utils.notion_filter_number(
                REPORT_FII_PVP_NOTION_PROPERTY, 1.0, notion_utils.FILTER_LESS_THAN_OR_EQUAL_TO
            )
        ),
        sort=[ notion_utils.notion_sort_desc(REPORT_FII_DY_NOTION_PROPERTY) ],
        page_size=15
    )