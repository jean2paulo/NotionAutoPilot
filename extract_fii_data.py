import requests
from bs4 import BeautifulSoup

# URL da página da qual você deseja recuperar o item
url = "https://statusinvest.com.br/fiagros/vgia11"

# Enviando uma solicitação GET para obter o conteúdo da página
response = requests.get(url)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisando o conteúdo da página com o Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Encontrando o elemento que contém o item desejado (substitua "SELETOR_CSS" pelo seletor correto)
    item_element = soup.select_one("SELETOR_CSS")
    
    # Verificando se o elemento foi encontrado
    if item_element:
        # Recuperando o texto do item
        item_text = item_element.get_text()
        print("Item recuperado:", item_text)
    else:
        print("Elemento não encontrado.")
else:
    print("Falha na solicitação. Código de status:", response.status_code)
