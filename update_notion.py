import gspread
from notion.client import NotionClient
import os

# Ler as variáveis de ambiente
# google_sheet_credentials_json = os.getenv('GOOGLE_SHEET_CREDENTIALS_JSON')
google_sheet_credentials_json = '{"type":"service_account","project_id":"notionautopilot","private_key_id":"c41612d9bebbd83a2549bc3d2362ac6f0ab00724","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC6FDE1AIRd3/aL\nwBPFsWmhr2ILcdqLlffNYtBCFJuHo6hl4nMxyIHEL58Y5VkjB+Yykn1HpfthespR\ndGnj6ta20UgIYNLeJFlyhneOU1VK/colMTWOM57ZNSEzje/M1KFWplcr5m1+LN59\n5dl3evfDDl4Et8t337F2T1Gdsz+nBsXdL3LIZxcrhHqN2SHcHSC2fW7btdqlVuJt\n/vYe0Uq/jA6K41e81kpPGLWgWt0WxCkHys1QpzVMn6IQxo84hy78RFRjqdpPBK1d\n2hVOqTRsoLn6HQWvr/jndZYF2eAqO2YQKnvorF4g8da1kfgs1G5KfKV/SEvFcnwa\nvmBL9RVXAgMBAAECggEAApcBieYhbaAWOWD944TnULbA1ANnsCurPV1EM78Bnq0J\n/0/QjOBRF/33JGXGuwIeMqw86y0RaiuUtN+GMSqn6y2ZHeEZalzyAG42v5fa94k7\n86oVKEkv0xPdC+vEkfcMQxaw7mTKu3ZjIzhL6ArQIjpaoW4eidtXJwD44577FrKI\ngnp4HWFOhR5zE5syN/XwkduxpH0dxnuk7wy4RqFqkersZhORCgD7np0hqWSke6EW\nnw0kPfkxPTL3QUqDyEoG4i1ax4BF1+nm6q7LXv95dWw2z5p+F1uUX0T1j7k/CmrH\nCrGLz9fr1fgY0bEh0I88GUIz+QBxFGja40jRfSs2gQKBgQDxtmlY8HM/rXsvD1RN\noegpBNtyU52McMk5eg1Om9IpXj/VY8qtmHOqTA99l18vLM3dN/2KzQVHOYfcFSl7\nVmrLYmcef7xFhwNp9uesUvvELHtUcgkJIOukWj+KX9Lhrnoqrk+j3vbswm+pjzL2\nDMCiEQaWB2++Xkfhws2lhXVuFwKBgQDFE+7vhiEqdI256607pJ2lynGKCoXOUm6C\nZLhPL4QLjF8keCW6vH6B0HXbbulgxJ6ET9AlRtrnIqztzmqKBH1JIvySMJmt3msR\nHH4nGI9u7VwPDCORWv03rZJyDr+nngmJp6ZHcTWWkMO/XMfoXbbK8BdsWZ1NgaJk\nqB6+fK9awQKBgCzt8Usc9u9BOgKXYN5FWDg3tOrdbA2s8VqDu3F/OWODJ25s7EG0\nctuW49I+juzf8SxLug9Q6MhCg2R/coSAnb1Mf0qGB+MMo6/Qu2Om0TG36vzZbaCK\nxAJ63BDGmxZkLkU8vYUCbve3dLYZ7ikaWbxGWekNXNIQCGCIq103H4rlAoGBAMCD\nV01Ndgp17pgmW4O+q2zvk/enjcvdBCyF3PElVlS9m5cRcrG2PdHrY6Wl833es4ZG\nPOqdC2rrmYd3suT9u7D850KbDRQmB+qgLa9dM4fFf78HOZtdCawg9sRKGffPzjtU\ntH5nXVSmN0Ewjesz2ELnQ8pIw/uZXZv8CoRDYjxBAoGBAOKtPS3trhXJbUb2kLn9\nnnoXCN5WdLJD9u9K9Vf2kI1ncZ83Ubk1+bHHFB3DMBoquO68anGgFVWxYcdFSnP5\nwTz7ot3V1AiSoQUDK8VEJWjIibm3z9AE3Wcmqzg4041HUror44LZVs8Mv707Dwx6\nXEYqJW/bXgfaweAX1L8VSFHG\n-----END PRIVATE KEY-----\n","client_email":"notionautopilot@notionautopilot.iam.gserviceaccount.com","client_id":"100393585357030456203","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/notionautopilot%40notionautopilot.iam.gserviceaccount.com","universe_domain":"googleapis.com"}'
notion_token = os.getenv('NOTION_TOKEN')

# Configurar cliente do Google Sheets e Notion
gc = gspread.service_account_from_dict(google_sheet_credentials_json)
client = NotionClient(token_v2=notion_token)

# ID da planilha do Google Sheets
spreadsheet_id = '1rKgwERiE6CQhK69sBun9N2dsGegAHTWctPS_KiHVM_8'
worksheet_name = 'QUOTES'  # Nome da planilha
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.worksheet(worksheet_name)

# Percorrer todas as linhas da planilha
data = worksheet.get_all_records()
for row in data:
    notion_page_url = row['URL']
    new_value = row['PRICE']

    # Pegar a página Notion correspondente
    notion_page = client.get_block(notion_page_url)

    # Atualizar o valor na propriedade "Price" da página no Notion
    notion_property = notion_page.collection.get_schema_property('Price')
    notion_page.set_property(notion_property['id'], new_value)
