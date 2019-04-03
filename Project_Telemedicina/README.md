
## Projeto - Data Engineer Telemedicina


Desenvolvido por: Bruno Scovoli Bruneli

Data Início: 25/03/2019

Data Término: 03/04/2019

### Overview


Neste projeto estaremos desenvolvendo duas APIs para extração e manipulação de dados importados de plataformas como Google e Twitter, com o objetivo de explorar alguns módulos e bibliotecas públicas utilizando linguagem Python. 

* API Pesquisa URL - Web Screaping: consiste em extrair dados de páginas web através de sua url, convertendo em informação estruturada para possíveis analises.

* API Pesquisa Twitter - Rest API: consiste em extrair dados de posts realizados na rede social - Twitter, com a finalidade de serem analisados e estruturados de forma a gerar informações condizentes aos envolvidos.

### Requerimentos

* Python 2.7 or 3.7+
* Ambiente Windows, Linux ou  MacOS
* Banco de Dados SQL Server

### Criando o Ambiente - (Virtualenv)

- Comando para instalação do virtualenv:
`pip install virtualenv`

- Criando um novo ambiente com o virtualenv chamado de "Project_Telemedicina":
`virtualenv Project_Telemedicina`

- Ativando o ambiente virtualenv na pasta "Project_Telemedicina\Scripts\":
`activate.bat`

- Com o ambiente isolado ativado, foi gerado o arquivo de dependencias a partir do comando:
`pip freeze > requirements.txt`

- Desativando o ambiente virtualenv na pasta "Project_Telemedicina":
`deactuvate`

- Para instalar as dependências do projeto no ambiente isolado, basta executar:
`pip install -r requirements.txt`


### Intruções de Execução

1. Criação da base de dados através do script SQL - disponível em: [Script_Query_SQL_Creation](https://github.com/brunobrunelli/TelemedicinaGit/blob/master/Project_Telemedicina/Python/Script_Query_SQL_Creation.sql)

2. Os arquivos **"Pesquisa_URL e Pesquisa_Twitter"** deverão ser alterados com o nome do servidor SQL no qual o script acima foi executado, assim como mostra a imagem a seguir apontando o lugar exado da alteração. Exemplo disponível em: [Alterar_Nome_Servidor](https://github.com/brunobrunelli/TelemedicinaGit/blob/master/Project_Telemedicina/Alterar_Nome_Servidor.png)

##### API Web Screaping:

3. Executável **"Pesquisa URL"** - disponível em: [Pesquisa_URL](https://github.com/brunobrunelli/TelemedicinaGit/blob/master/Python/Pesquisa_URL.py)

##### API Twitter:

4. Caso o arquivo **"Credenciais Twitter"** não esteja criado no diretório, o mesmo pode ser criado a partir do executável **"Criar Credencias Twitter"** - disponível em: [Criar_Credenciais_Twitter](https://github.com/brunobrunelli/TelemedicinaGit/blob/master/Project_Telemedicina/Python/Criar_Credenciais_Twitter.py)

5. Arquivo .json com as credenciais de acesso a API do Twitter - disponível em: [Credenciais_Twitter](https://github.com/brunobrunelli/TelemedicinaGit/blob/master/Python/Credenciais_Twitter.json)

6. Executável **"Pesquisa Twitter"** - disponivel em: [Pesquisa_Twitter](https://github.com/brunobrunelli/TelemedicinaGit/blob/master/Project_Telemedicina/Python/Pesquisa_Twitter.py)


### Módulos e Bibliotecas do Python Utilizadas no projeto

`pip install regex - https://pypi.org/project/regex/`

`pip install pyodbc - https://pypi.org/project/pyodbc/`

`pip install pandas - https://pypi.org/project/pandas/`

`pip install jsonschema - https://pypi.org/project/jsonschema/`

`pip install urllib3 - https://pypi.org/project/urllib3/`

`pip install tldextract - https://pypi.org/project/tldextract/`

`pip install urlopen - https://pypi.org/project/urlopen/`

`pip install bs4 - https://pypi.org/project/bs4/`

`pip install google - https://pypi.org/project/google/`

`pip install search-google	- https://pypi.org/project/search-google/`

`pip install google-search - https://pypi.org/project/google-search/`

`pip install twython - https://pypi.org/project/twython/`




