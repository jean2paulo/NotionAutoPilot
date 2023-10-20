from notion.tasks import utils as task_utils
from notion import utils as notion_utils

NOTION_CHECK_TASKS_BOT_TERM = "notion_check_tasks"

def request_project_option(message, bot, message_handler):
    # Bot envia mensagem perguntando sobre qual projeto?
    sent_msg = bot.send_message(
        message.chat.id, 
        task_utils.PROJECT_REQUEST_MESSAGE, 
        parse_mode="Markdown"
    )
    # Bot registra o um handler para a resposta
    bot.register_next_step_handler(
        sent_msg, 
        response_project_option, message_handler
    )

def response_project_option(message, message_handler):
    message_handler(
        message, 
        task_utils.PROJECT_RESPONSE_OPTIONS.get(
                int(message.text)
            )
        )


def check_tasks(notion, message, bot):
    request_project_option(message, bot,  
            lambda message, pageId: 
                response_task(notion, message, bot, pageId)
        )
    
# Notion Queries

def response_task(notion, message, bot, pageId):        
    data = notion_utils.notion_query(notion, task_utils.NOTION_PROJECT_PAGE_ID,
            filter=notion_utils.notion_filter_and(
                notion_utils.notion_filter_relation("Projeto", pageId),
                notion_utils.notion_filter_status("Status", task_utils.SPRINT_STATUS)
            ))
    
    full_message = "✅ Tarefas:"

    for result in data["results"]:
        title = notion_utils.extract_title(result, "Nome")
        full_message += f"\n⏺ {title}"

    bot.send_message(
        message.chat.id, 
        full_message,
        parse_mode="Markdown"
    )

def check_all_tasks(notion):        
    data = notion_utils.notion_query(notion, task_utils.NOTION_PROJECT_PAGE_ID,
        filter=notion_utils.notion_filter_status("Status", task_utils.SPRINT_STATUS),
        sort=[notion_utils.notion_sort_asc("Projeto")]
    )
    if(len(data["results"]) > 0):
        full_message = "✔️ Tarefas"
        last_relation_id = -1
        for result in data["results"]:
            relation_id = notion_utils.extract_relation_id(result, "Projeto")
            if relation_id != last_relation_id:
                project = task_utils.extract_project_name(relation_id)
                full_message += f"\n{project}\n"
                last_relation_id = relation_id
                
            title = notion_utils.extract_title(result, "Nome")
            full_message += f"\n→ {title}"
    else:
        full_message = "✔️ Sem tarefas!"
    
    return full_message
