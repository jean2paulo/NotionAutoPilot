import uuid

# Projects Notion Page


# Projects
SPRINTER_PAGE_ID = "144133c3-3a5a-4938-b876-d1cda4d047de"
XP_PAGE_ID = "5da4863850d849688639d50845482c27"
DEV_PAGE_ID = "2daa2ac5-b92b-483f-8716-25893df4ebd6"
NEW_ZEELAND_PAGE_ID = "166e2972-07e5-4401-85e1-df57f468aa91"
SELF_IMPROVE_PAGE_ID = "e9b63057-6d94-4688-a2ee-a410ca745183"
CHILE_PAGE_ID = "8a623559-e5fe-4cbf-a413-2efb4edbcba9"
SAUDE_PAGE_ID = "97333f1c-5770-4aed-a0a1-cb3d5ba4066f"
BRAZIL_PAGE_ID = "b90f9655-4fc0-4a69-9efd-8d94e62498fb"
FINANCAS_PAGE_ID = ""
DIA_DIA_PAGE_ID = "c73241a9-ac26-4748-b6c2-b11030ea67ea"
NOTION_PAGE_ID = "fe1636b4-3233-4202-b8ef-60219e00752b"
VIAJA_JEAN_PAGE_ID = "958c9312-893c-4514-9731-34880728dd70"



# Request
PROJECT_REQUEST_MESSAGE = "Qual Projeto?\n1- Finanças\n2- Sprinter\n3- Dev\n4- XP\n5- Self-Improve\n6- Chile\n7- Saude"
PROJECT_RESPONSE_OPTIONS = {
        1: FINANCAS_PAGE_ID,
        2: SPRINTER_PAGE_ID,
        3: DEV_PAGE_ID,
        4: XP_PAGE_ID,
        5: SELF_IMPROVE_PAGE_ID,
        6: CHILE_PAGE_ID,
        7: SAUDE_PAGE_ID,
    }

def format_page_id(notion_page_id):
    return f"{notion_page_id[:8]}-{notion_page_id[8:12]}-{notion_page_id[12:16]}-{notion_page_id[16:20]}-{notion_page_id[20:]}"

def create_task(title):
    return {
        "parent": {
            "database_id": NOTION_PROJECT_PAGE_ID
        },
        "properties": { 
            "title": { 
                "title": [ 
                    {
                        "type": "text", "text": { 
                            "content": title
                        } 
                    } 
                ] 
            } 
        } 
    }

def searchQuery(pageId, status):
    return { 
            "database_id": NOTION_PROJECT_PAGE_ID,
            #"page_size": 100,
            "filter": { 
                 "and": [
                     {
                        "property": "Projeto",
                        "relation": {
                            "contains": pageId
                            #"is_not_empty": True
                        } 
                    },{
                        "property": "Status",
                        "status": {
                            "does_not_equal": status
                        }
                    }
                 ]
            } 
        }
    
def format_message_title(title):
    return f"***️⃣ {title}**\n---------\n"


def extract_project_name(page_id):
    if(page_id == SPRINTER_PAGE_ID):
        return '🚐 Sprinter'
    elif(page_id == FINANCAS_PAGE_ID):
        return '💰 Finanças'
    elif(page_id == SELF_IMPROVE_PAGE_ID):
        return '🧘🏻 Self-Improve'
    elif(page_id == CHILE_PAGE_ID):
        return '🇨🇱 Chile'
    elif(page_id == SAUDE_PAGE_ID):
        return '🏥 Saude'
    elif(page_id == NOTION_PAGE_ID):
        return '📚 Notion'    
    elif(page_id == DEV_PAGE_ID):
        return '🖥️ Dev'    
    elif(page_id == DIA_DIA_PAGE_ID):
        return '☀️ Dia a dia'
    elif(page_id == BRAZIL_PAGE_ID):
        return '🇧🇷 Brasil'
    elif(page_id == VIAJA_JEAN_PAGE_ID):
        return '📸 @viaja.jean'  
    else:
        return page_id