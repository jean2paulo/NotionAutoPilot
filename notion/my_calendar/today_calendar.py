from notion.commons import utils as notion_utils
from .constants import * 
from .strings import *

def get_today_calendar_message(notion):
     total_data = get_today_calendar(notion)
     return format_today_calendar_message(total_data)

def get_today_calendar(notion):
    return notion_utils.notion_query(notion, CALENDAR_PAGE_ID, 
        notion_utils.notion_filter_checkbox(TODAY_NOTION_PROPERTY, True)
    )

def format_today_calendar_message(data):
    if(len(data[RESULTS]) > 0):
        calendar_message = TITLE_TEXT
        for result in data[RESULTS]:
            name = notion_utils.extract_title(result, DESCRIPTION_NOTION_PROPERTY)
            calendar_message += ITEM_TEXT_FORMAT % name
    else:
        calendar_message = NO_DATA_TEXT
    
    return calendar_message