# ----------------------------------------------------------------------------------------------------------

# Programa 1 - Leitura e Gravação de Dados - Telemedicina

# Criado por: Bruno Scovoli Bruneli
# Data Criação: 01/04/2019

# Descrição: Realizaremos a consulta da palavra "Telemedicina" no campo de busca do Google e retornaremos
# os 100 primeiros registros, armazenando em uma base de dados SQL Server a url, o domínio e o conteúdo 
# de cada site retornado com base na ordem de exibição do Google.

# ----------------------------------------------------------------------------------------------------------

# Importação dos Módulos e Bibliotecas
import re
import pyodbc 
import pandas as pd
import urllib3
import tldextract
from urllib.request import urlopen
from bs4 import BeautifulSoup
from googlesearch import search

# Conexão com o Banco de Dados - SQL Server:
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-2TEIT25\SQLSERVERLOCAL;'
    'DATABASE=DB_TELEMEDICINA;'
    'UID=adm;'
    'PWD=admin')

# Abrir conexão com o banco: 
cursor = conn.cursor()

# Realizamos um truncate na tabela para gravar os dados mais atualizados:
sql_command = ("TRUNCATE TABLE dbo.TB_URL_TELEMEDICINA")

# Executa comando Truncate:
cursor.execute(sql_command)

# Criamos um comando de Insert dos dados:
sql_command = ("INSERT INTO dbo.TB_URL_TELEMEDICINA (INDICE_GOOGLE,URL,DOMINIO,CONTEUDO) VALUES (?,?,?,?)")

# Desabilitando warnings retornados pelo Python:
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----------------------------------------------------------------------------------------------------------
# Lógica para leitura das URLs retornadas na busca pelo termo "Telemedicina"

# Termo a ser pesquisado
query = "telemedicina"
lista_valores = []
lista_web_error = []
index=0

print('\nInicia processo de Leitura/Gravação dos dados...')

for url in search(query, stop=100):
    texto_http = []
    my_list_http = []

    try:
        # Realizamos a leitura de cada HTML:
        html = urlopen(url).read()
        soup = BeautifulSoup(html,"lxml")

        # Removemos algumas tags indesejadas em nosso retorno do HTML:
        for script in soup(["script", "style", "class"]):
            script.extract()

        # Inserimos em uma lista somente o conteúdo desejado do HTML:
        for i in range(len(soup.find_all(['title', 'p']))):
            texto_http.append(soup.find_all(['title', 'p'])[i].get_text())

        # Inserimos toda lista retornada em uma valiárel:
        my_list_http = ' '.join(texto_http)
        
        # Extração do domínio através do módulo tldextract:
        dominio_name = tldextract.extract(url)
        dominio = (dominio_name.domain+'.'+dominio_name.suffix)
        
        # Valores a serem inseridos no Banco de Dados
        values = [index,url,dominio,my_list_http]

        # Inserimos todos os valores em uma lista:
        lista_valores.append(values)
        
        # Executamos o comando de INSERT dos dados no banco, passando os valores a serem inseridos na tabela:
        cursor.execute(sql_command,values)
        
        # Acrecentamos +1 ao indice que identifica a ordem com que cada URL é lida:
        index +=1

    except:
        # Gravamos as URLs que retornaram erro ao serem acessados (erro SSH / Certificado):
        lista_web_error.append(url)

# ----------------------------------------------------------------------------------------------------------
# Mensagem de Processo Completo:
print('\nDados Inseridos com Sucesso...')

# Impressão da quantidade de URLs gravadas no banco e que retornaram erro:
print('\nQtde. URLs inseridas: ' + str(len(lista_valores)))
print('Qtde. URLs com erro: ' + str(len(lista_web_error)))

# Fechar Conexao com o Banco de Dados
conn.commit()
conn.close()
