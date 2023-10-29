from notion.commons import utils as notion_utils
from notion.tasks import utils as task_utils
from .constants import * 
from .strings import *

def get_all_tasks_message(notion):
   total_data = get_all_tasks(notion)
   return format_all_tasks_message(total_data)
   

def get_all_tasks(notion):
    return notion_utils.notion_query(notion, NOTION_PROJECT_PAGE_ID,
        filter=notion_utils.notion_filter_status(TASKS_STATUS_NOTION_PROPERTY, SPRINT_STATUS),
        sort=[notion_utils.notion_sort_asc(TASKS_PROJECT_NOTION_PROPERTY)]
)

def format_all_tasks_message(data):
    if(len(data[RESULTS]) > 0):
        tasks_message = TITLE_TEXT
        last_relation_id = -1
        
        for result in data[RESULTS]:
            relation_id = notion_utils.extract_relation_id(result, TASKS_PROJECT_NOTION_PROPERTY)
            if relation_id != last_relation_id:
                project = task_utils.extract_project_name(relation_id)
                tasks_message += PROJECT_TITLE_FORMAT % project
                last_relation_id = relation_id
                
            title = notion_utils.extract_title(result, TASKS_NAME_NOTION_PROPERTY)
            tasks_message += ITEM_TEXT_FORMAT % title
    else:
        tasks_message = NO_DATA_TEXT

    return tasks_message