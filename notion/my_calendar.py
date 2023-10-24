import utils as notion_utils

# Projects Notion Page
CALENDAR_PAGE_ID = "2f507df1949845c0ae7628401b9f273b"

def check_today_calendar(notion):
    data = notion_utils.notion_query(notion, CALENDAR_PAGE_ID, 
            notion_utils.notion_filter_checkbox("Hoje", True)
        )
    full_message = ''
    if(len(data["results"]) > 0):
        full_message = "🗓️ Eventos"
        for result in data["results"]:
            name = notion_utils.extract_title(result, "Descriçao")
            full_message += f"\n→ {name}" 
    else:
        full_message = "🗓️ Sem eventos!"

    return full_message