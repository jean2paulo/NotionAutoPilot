from notion_client import Client

notion_page_id = "1c0103c3ddb944c38f84b1b1c9dc68cc"
formatted_page_id = f"{notion_page_id[:8]}-{notion_page_id[8:12]}-{notion_page_id[12:16]}-{notion_page_id[16:20]}-{notion_page_id[20:]}"

try :
  my_page = notion.databases.query(
    **{
      "database_id": formatted_page_id,
      "filter": {
        "property": "Hoje",
          "checkbox": true
      },
    }
  )
  
  print(f"✓ {name}: {price}")
except APIResponseError as error:
    if error.code == APIErrorCode.ObjectNotFound:
      print("Sem aniversarios hoje!")
    else:
        # Other error handling code
      print(f"Error: ")
      
