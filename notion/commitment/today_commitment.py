from notion.commons import utils as notion_utils
from .constants import * 
from .strings import *

def get_today_commitment_message(notion):
     total_data = get_today_commitment(notion)
     return format_today_commitment_message(total_data)

def get_today_commitment(notion):
    return notion_utils.notion_query(notion, COMMITMENT_PAGE_ID, 
        notion_utils.notion_filter_checkbox(TODAY_NOTION_PROPERTY, True)
    )

def format_today_commitment_message(data):
    if(len(data[RESULTS]) > 0):
        commitment_message = TITLE_TEXT
        for result in data[RESULTS]:
            name = notion_utils.extract_title(result, DESCRIPTION_NOTION_PROPERTY)
            commitment_message += ITEM_TEXT_FORMAT % name
    else:
        commitment_message = NO_DATA_TEXT
    
    return commitment_message