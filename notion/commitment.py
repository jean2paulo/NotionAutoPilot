from notion import utils as notion_utils

# Notion Page ID
COMMITMENT_PAGE_ID = "b6b050fe49f84edab2f271dca493b9fe"

def check_today_commitment(notion):
    data = notion_utils.notion_query(notion, COMMITMENT_PAGE_ID, 
            notion_utils.notion_filter_checkbox("Hoje", True)
        )
    full_message = ''
    if(len(data["results"]) > 0):
        full_message = "🔄 Compromissos"
        for result in data["results"]:
            name = notion_utils.extract_title(result, "Descriçao")
            full_message += f"\n⏺ {name}" 
    else:
        full_message = "🔄 Sem compromisso!"
    
    return full_message