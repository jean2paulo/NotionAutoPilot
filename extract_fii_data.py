import requests
from bs4 import BeautifulSoup

# URL da página da qual você deseja recuperar o item
url = "https://www.fundsexplorer.com.br/funds/vino11"

# Enviando uma solicitação GET para obter o conteúdo da página
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, headers=headers)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisando o conteúdo da página com o Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrando todos os elementos que correspondem ao seletor CSS (substitua "SELETOR_CSS" pelo seletor correto)
    elements = soup.select("<div class=\"indicators_box\">")
    
    # Verificando se elementos foram encontrados
    if elements:
        for element in elements:
            # Recuperando o texto de cada elemento
            element_text = element.get_text()
            print("Elemento encontrado:", element_text)
    else:
        print("Elementos não encontrados.")
    
    # Encontrando o elemento que contém o item desejado (substitua "SELETOR_CSS" pelo seletor correto)
    #item_element = soup.select_one("SELETOR_CSS")
    
    # Verificando se o elemento foi encontrado
    #if item_element:
        # Recuperando o texto do item
        #item_text = item_element.get_text()
        #print("Item recuperado:", item_text)
    #else:
        #print("Elemento não encontrado.")
else:
    print("Falha na solicitação. Código de status:", response.status_code)
