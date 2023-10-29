from notion.commons import utils as notion_utils
from .constants import * 
from .strings import *

def update_fiis(notion, content):
     for fii in content:
        page_id = fii
        #notion_utils.notion_update(notion, page_id)

def get_fiis_id(notion):
    data = _get_fiis(notion)
    fiis = []
    if(len(data[RESULTS]) > 0):
        for result in data[RESULTS]:
            name = notion_utils.extract_title(result, FII_NAME_NOTION_PROPERTY)
            id = "123"
            print(result)
            # TODO extract id
            fiis.append({
                name: id
            })

    return fiis

# Private Methods

def _get_fiis(notion):
    return notion_utils.notion_query(notion, FIIS_PAGE_ID)