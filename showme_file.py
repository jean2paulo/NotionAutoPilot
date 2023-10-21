import os
import json

# Ler as variáveis de ambiente
credentials_file = os.getenv('GOOGLE_CLOUD_CREDENTIALS_FILE')

# Abre o arquivo JSON
with open(credentials_file, 'r') as arquivo:
    # Carrega o conteúdo do arquivo JSON
    dados = json.load(arquivo)

# Mostra o conteúdo
print(dados)