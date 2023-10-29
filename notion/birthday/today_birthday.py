from notion.commons import utils as notion_utils
from .constants import * 
from .strings import *

def get_today_birthday_message(notion):
     total_data = get_today_birthday(notion)
     return format_today_birthday_message(total_data)

def get_today_birthday(notion):
    return notion_utils.notion_query(notion, BIRTHDAY_PAGE_ID, 
        notion_utils.notion_filter_checkbox(TODAY_NOTION_PROPERTY, True)
    )

def format_today_birthday_message(data):
    if(len(data[RESULTS]) > 0):
        birthday_message = TITLE_TEXT
        for result in data[RESULTS]:
            name = notion_utils.extract_title(result, NAME_NOTION_PROPERTY)
            birthday_message += ITEM_TEXT_FORMAT % name
    else:
        birthday_message = NO_DATA_TEXT

    return birthday_message