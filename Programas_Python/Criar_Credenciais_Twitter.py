import json

# Credenciais do Twitter, criando arquivo .json:
credentials = {}  
credentials['CONSUMER_KEY'] = "mqxs3gducYrTWafV8NY4Fauzx"  
credentials['CONSUMER_SECRET'] = "z8iSsFQiwAkwmW2eQV5td71e5q5EMqE4qBUhcdfeKFlSzDMODP"  
credentials['ACCESS_TOKEN'] = "870309613836673025-KHzLHf1nnQ59FKEkMz9BPyCvRQS8xPY"  
credentials['ACCESS_SECRET'] = "fkcUgV9cHxBrDUIYDiNd3tof4pifGYr4bcCrN8uJ9t5uO"

# Salvar valores das credenciais de acesso:
with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)