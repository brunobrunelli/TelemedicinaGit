# ----------------------------------------------------------------------------------------------------------

# Step 1 - Criação do Arquivo Credenciais Twitter

# Criado por: Bruno Scovoli Bruneli
# Data Início: 31/03/2019
# Data Término: 31/04/2019

# Descrição: Nesta API iremos gerar o arquivo que será importado na API de pesquisa, contendo as credenciais
# de acesso ao Twitter.

# ----------------------------------------------------------------------------------------------------------

# Importação dos Módulos e Bibliotecas
import json

# Credenciais do Twitter, criando arquivo .json:
credentials = {}  
credentials['CONSUMER_KEY'] = "mqxs3gducYrTWafV8NY4Fauzx"  
credentials['CONSUMER_SECRET'] = "z8iSsFQiwAkwmW2eQV5td71e5q5EMqE4qBUhcdfeKFlSzDMODP"  
credentials['ACCESS_TOKEN'] = "870309613836673025-KHzLHf1nnQ59FKEkMz9BPyCvRQS8xPY"  
credentials['ACCESS_SECRET'] = "fkcUgV9cHxBrDUIYDiNd3tof4pifGYr4bcCrN8uJ9t5uO"

# Salvar valores das credenciais de acesso em um arquivo de formato .json:
with open("Credenciais_Twitter.json", "w") as file:  
    json.dump(credentials, file)