# Importação dos Módulos e Bibliotecas
import pyodbc
import pandas as pd
import collections
import tldextract

# Conexão com o Banco de Dados - SQL Server:
connection = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-2TEIT25\SQLSERVERLOCAL;'
    'DATABASE=DB_TELEMEDICINA;'
    'UID=adm;'
    'PWD=admin')

# Abrir conexão com o banco: 
cursor = connection.cursor()

# ----------------------------------------------------------------------------------------------
# Descrição: Realizaremos a extração dos dados de um banco SQL Server lendo todos os registros
# da tabela TB_URL_TELEMEDICINA, selecionando os domínios mais frequentes gravados no banco.

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

# Imprime o dataFrame referente aos dados de Domínio:
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
not_words = ['a','e','i','o','u','os','da','das','de','do','no','na','nas','que','uma','um','já','é','em','até','ou','com','como','para','null','0','r','por','as','the','dos','ser','à','mais','se','não','ao','in','and','of','to','são','sua','entre','sobre','pela','pelo','pode','for','ele','você','are','with','nos','aos','seu','também','r]','[1]','[null','às']

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

# Imprimimos o conteúdo do Dataframe:
print(dfConteudo)

