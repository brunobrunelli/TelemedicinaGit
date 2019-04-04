# ----------------------------------------------------------------------------------------------------------

# Step 1 - Extração e Carga dos Dados - Telemedicina

# Criado por: Bruno Scovoli Bruneli
# Data Início: 25/03/2019
# Data Término: 31/03/2019

# Descrição: Nesta API realizaremos a consulta da palavra "Telemedicina" no campo de busca do Google e retornaremos
# os 100 primeiros registros, armazenando em uma base de dados SQL Server a url, o domínio e o conteúdo 
# de cada site retornado com base na ordem de exibição do Google.

# ----------------------------------------------------------------------------------------------------------

# Importação dos Módulos e Bibliotecas
import re
import pyodbc 
import pandas as pd
import urllib3
import tldextract
import collections
from urllib.request import urlopen
from bs4 import BeautifulSoup
from googlesearch import search

# Imprime Inicio do Step 1:
print('\nInício - Step 1 - Extração e Carga dos Dados')

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
# Descriçãp: Lógica para leitura das URLs retornadas do pelo Google na busca pelo termo "Telemedicina".

# Termo a ser pesquisado
query = "telemedicina"
lista_valores = []
lista_web_error = []
index=0

print('\nInicia processo de Leitura/Gravação dos dados...')

# Início do loop, percorrendo as 100 primeiras páginas:
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

# Impreme quantidade de URLs gravadas no banco e que retornaram erro:
print('\nQtde. URLs inseridas: ' + str(len(lista_valores)))
print('Qtde. URLs com erro: ' + str(len(lista_web_error)))

# Commit dos dados inseridos no banco:
conn.commit()

# ----------------------------------------------------------------------------------------------
# Step 2 - Leitura e Exibiçãp de Dados armazenados no Banco - Telemedicina

# Descrição: Realizaremos a extração dos dados de um banco SQL Server lendo todos os registros
# da tabela TB_URL_TELEMEDICINA, selecionando os domínios mais frequentes gravados no banco.

print('\nInício - Step 2 - Leitura e Exibição dos Dados')

# Comando SQL para extrair os Domínios da tabela TB_URL_TELEMEDICINA:
sql_command_link = """
    SELECT COUNT(*) AS QTD, DOMINIO
    FROM dbo.TB_URL_TELEMEDICINA
    GROUP BY DOMINIO
    ORDER BY QTD DESC
"""
# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()

# Converter lista de registros em um Dataframe:
dfDominio = pd.DataFrame.from_records(return_query_link,columns=['Frequencia','Dominio'])

# 1) Imprime lista de Domínios mais frequentes referente ao termo "telemedicina":
print('\nImprime lista de domínios mais frequentes:')
print(dfDominio)

# ----------------------------------------------------------------------------------------------

# Descrição: Realizaremos a extração dos dados de um banco SQL Server lendo todos os registros
# da tabela TB_URL_TELEMEDICINA, retornando uma lista dos 100 temos mais utilizados referente 
# ao conteúdo das páginas.

# Comando SQL para retornar os registros da tabela:
sql_command_conteudo = "SELECT CONTEUDO FROM dbo.TB_URL_TELEMEDICINA ORDER BY INDICE_GOOGLE"

# Captura o retorno da consulta e grava em uma lista:
return_query_conteudo = cursor.execute(sql_command_conteudo).fetchall()

# Concatena todo retorno em uma string para tratamento dos conteúdos:
lista_result = ' '.join(str(v) for v in return_query_conteudo)

# Criamos duas listas para limpeza dos caracteres indesejados em nosso conteúdo:
lista_remove_1 = ['[',']']
lista_remove_2 = [',','.','(',')',"/","'",'etc','\\xa0','‘','’','”','“','\\n','   ','…','©',':','|','?','!','–','-','\\s']

# Realizamos a limpeza do conteúdo - lista 1:
for i in lista_remove_1:
    if i == '[':
        lista_result = lista_result.replace(i,' [')
    else:
        lista_result = lista_result.replace(i,'] ')

# Realizamos a limpeza do conteúdo - lista 2:
for i in lista_remove_2:
    lista_result = lista_result.replace(i,'')    

# Separamos todos conteúdo da lista:
lista_result = lista_result.split()

# Criamos uma lista de palavras e termos indesejados:
list_words = []
not_words = ['a','e','i','o','u','os','da','das','de','do','no','na','nas','que','uma','um','já','é','em','até','ou','com','como','para','null','0','r','por','as','the','dos','ser','à','mais','se','não','ao','in','and','of','to','são','sua','entre','sobre','pela','pelo','pode','for','ele','você','are','with','nos','aos','seu','também','r]','[1]','[null','às','is','at','or','can','that','by','was','be','an','also','from','not','this','it']

# Percorremos toda a lista removendo as palavras indesejadas,
# criando uma nova lista com os dados limpos:
for i in lista_result:
    if i.lower() not in not_words:
        list_words.append(i.lower())

# Criamos um dicionário para armazenas a quantidade de vezes que
# o termo aparece no conteúdo:
count_word = dict()

# Realizamos a contagem de cada termo:
for word in list_words:
    if word in count_word:
        count_word[word] += 1
    else:
        count_word[word] = 1

# Com base no dicionário de palavras/termos, criamos um DataFrame populado com esses dados:
dfConteudo = pd.DataFrame(count_word.items(),columns=['Texto','Qtde'])

# Ordenamos o Dataframe com base na coluna "Qtde" selecionando somente os 100 primeiros termos:
dfConteudo = dfConteudo.sort_values(by=['Qtde'],ascending=False).head(100)

# 2) Imprime os 100 termos mais utilizados referente a "telemedicina":
print('\nImprime 100 termos mais utilizados:')
print(dfConteudo.head(100))

# ----------------------------------------------------------------------------------------------
# Fecha conexão com o banco de dados:
cursor.close()
conn.close()
