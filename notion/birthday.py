from notion import utils as notion_utils

# Notion Page ID
BIRTHDAY_PAGE_ID = "40320b7c1ad24942980da4714b1ec138"

def check_today_birthday(notion):
    data = notion_utils.notion_query(notion, BIRTHDAY_PAGE_ID, 
            notion_utils.notion_filter_checkbox("Hoje", True)
        )
    full_message = ''
    if(len(data["results"]) > 0):
        full_message = "🎂 Aniversarios"
        for result in data["results"]:
            name = notion_utils.extract_title(result, "Nome")
            full_message += f"\n⏺ {name}" 
    else:
        full_message = "🎂 Sem aniversariantes!"

    return full_message