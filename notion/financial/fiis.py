from notion.commons import utils as notion_utils
from .constants import *
from .strings import *

def get_fundamentus_fiis_id(notion):
    data = _get_fundamentus_fiis(notion)
    fundamentus_fiis = []
    if (len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            id = notion_utils.extract_id(result)
            name = notion_utils.extract_title(result, FII_NAME_NOTION_PROPERTY)
            fundamentus_fiis.append({
                'id': id,
                'name': name,
            })

    return fundamentus_fiis

def update_fundamentus_fiis(notion, page_id, properties):
    notion_utils.notion_update(
        notion,
        page_id,
        properties={
            **notion_utils.notion_update_string(FII_SEGMENT_NOTION_PROPERTY, properties['segmento']),
            **notion_utils.notion_update_number(FII_PRICE_NOTION_PROPERTY, properties['cotacao']),
            **notion_utils.notion_update_number(FII_VP_COTA_NOTION_PROPERTY, properties['vp_cota']), 
            **notion_utils.notion_update_number(FII_PVP_NOTION_PROPERTY, properties['pvp']), 
            **notion_utils.notion_update_number(FII_DY_NOTION_PROPERTY, properties['dy'])  
        }
    )

# Private Methods

def _get_fundamentus_fiis(notion):
    return notion_utils.notion_query(
        notion, FIIS_PAGE_ID,
    )