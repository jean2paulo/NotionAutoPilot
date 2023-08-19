import requests
from bs4 import BeautifulSoup

# URL da página da qual você deseja recuperar o item
url = "https://www.fundsexplorer.com.br/funds/vino11"

# Enviando uma solicitação GET para obter o conteúdo da página
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url, headers=headers)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analisando o conteúdo da página com o Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrando todos os elementos que correspondem ao seletor CSS (substitua "SELETOR_CSS" pelo seletor correto)
    price = soup.find("span", class_="price")

    lastDy = soup.find_all("span", class_="indicator-value")

    print("Preço": price.text.replace(" ", ""))
    print("Ultimo rendimento": lastDy[1].text.replace(" ", ""))
    
    
else:
    print("Falha na solicitação. Código de status:", response.status_code)
