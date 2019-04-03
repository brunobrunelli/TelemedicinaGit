# ----------------------------------------------------------------------------------------------------------

# Step 1 - Extração e Carga dos Dados - Telemedicina - Twitter API

# Criado por: Bruno Scovoli Bruneli
# Data Início: 31/03/2019
# Data Término: 03/04/2019

# Descrição: Nesta API realizaremos a consulta da palavra "Telemedicina" no Twitter e retornaremos os 100
# primeiros registros mais recentes, armazenando em uma base de dados SQL Server o usário, data e 
# hora da postagem e o conteúdo postado.

# ----------------------------------------------------------------------------------------------------------

# Importação dos Módulos e Bibliotecas
from twython import Twython
import json
import pandas as pd
import time
import pyodbc 

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
sql_command = ("TRUNCATE TABLE dbo.TB_TWEETS")

# Executa comando Truncate:
cursor.execute(sql_command)

# Criamos um comando de Insert dos dados:
sql_command = ("INSERT INTO dbo.TB_TWEETS ([USUARIO],[DATA],[HORARIO],[POSTAGEM]) VALUES (?,?,?,?)")

# Extraindo as credenciais de acesso do Twitter de um arquivo .json:
with open("Credenciais_Twitter.json", "r") as file:  
    creds = json.load(file)

# Instanciando um objeto twython:
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# ----------------------------------------------------------------------------------------------------------
# Descrição: Lógica para retornar os Tweets que possuem o termo "telemedicina". Extraindo os dados e através
# de um módulo instanciado do Twitter onde podemos realizar requisições na aplicação e retornar os dados
# desejados, como: usuário, data e hora da postagem e o conteúdo postado.

# Criando query com os parametros a serem passados no método:
query = {'q': 'telemedicina','count':100,'lang': 'pt'}

# Dicionário para armazenar os tweets:
dict_twitter = {'usuario': [], 'data': [], 'horario':[], 'postagem': []}

lista_twitter = []
try:
    # Pesquisando o termo "telemedicina" e retornando os 1000 tweets: 
    for status in python_tweets.search(**query)['statuses']:  
        usuario = (status['user']['screen_name'])
        data = (time.strftime('%Y-%m-%d', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
        horario = (time.strftime('%H:%M:%S', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
        postagem = (status['text'])

        # Gravamos os dados de retorno em uma lista
        values = [usuario, data, horario, postagem]
        lista_twitter.append(values)

        # Insere os dados no Banco SQL através do comando setado anteriormente, passando os valores a serem
        # inseridos na tabela:
        cursor.execute(sql_command, usuario, data, horario, postagem)
except:
    # Caso ocorra algum erro no processo de leitura dos Tweets:
    print('\nExcessão: Erro ao realizar busca de Tweets.')

# Estruturar o dado retornado nos tweets armazenando em um Dataframe:
#df = pd.DataFrame(dict_twitter)  
#df = df.sort_values(['data','horario'], ascending=False)   

# Mensagem de Processo Completo:
print('\nDados Inseridos com Sucesso...')

# Commit dos dados incluídos no banco:
conn.commit()

# ----------------------------------------------------------------------------------------------------------
# Step 2 - Leitura e Exibição dos dados do Banco SQL - Pesquisa Tweet:

# Descrição: Realizaremos a leitura dos dados gravados na tabela TB_TWEETS para análise e extração.

# Imprime Inicio do Step 2:
print('\nInício - Step 2 - Leitura e Exibição dos Dados')

# Comando SQL para extrair os dados dos usuários com mais tweets:
sql_command_link = """
    SELECT 
        COUNT(*) AS QTD_TWEET, 
        USUARIO
    FROM [dbo].[TB_TWEETS]
    GROUP BY USUARIO
    ORDER BY QTD_TWEET DESC
"""

# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()

# Converter lista de registros em um Dataframe:
dfQtdeTweet = pd.DataFrame.from_records(return_query_link,columns=['Quantidade_Tweet','Usuario'])

# Imprime lista de usuários com maior número de postagens com o termo "telemedicina":
print('\nLista dos *usuários* com maior número de postagens:')
print(dfQtdeTweet.head(10))

# ----------------------------------------------------------------------------------------------------------
# Comando SQL para extrair os dados do dia da semana com mais tweets:
sql_command_link = """
SELECT 
    COUNT(*) AS QTD_TWEET,
    CASE DATEPART(dw,[DATA])
        WHEN (1) THEN 'Domingo'
        WHEN (2) THEN 'Segunda-Feira'
        WHEN (3) THEN 'Terça-Feira'
        WHEN (4) THEN 'Quarta-Feira'
        WHEN (5) THEN 'Quinta-Feira'
        WHEN (6) THEN 'Sexta-Feira'
        WHEN (7) THEN 'Sabado'
    END DIA_DA_SEMANA
FROM dbo.TB_TWEETS
GROUP BY
    CASE DATEPART(dw,[DATA])
        WHEN (1) THEN 'Domingo'
        WHEN (2) THEN 'Segunda-Feira'
        WHEN (3) THEN 'Terça-Feira'
        WHEN (4) THEN 'Quarta-Feira'
        WHEN (5) THEN 'Quinta-Feira'
        WHEN (6) THEN 'Sexta-Feira'
        WHEN (7) THEN 'Sabado'
    END
ORDER BY QTD_TWEET DESC
"""

# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()

# Converter lista de registros em um Dataframe:
dfDiaSemana = pd.DataFrame.from_records(return_query_link,columns=['Quantidade_Tweet','Dia_Semana'])

# Imprime a quantidade de Tweets durante os dias da semana:
print('\nLista dos *dias* com maior número de postagens:')
print(dfDiaSemana)

# ----------------------------------------------------------------------------------------------------------
# Comando SQL para extrair os dados das horas do dia com mais tweets:
sql_command_link = """
    SELECT 
        COUNT(*) AS QTD_TWEET,
        DATEPART(HOUR,HORARIO) AS HORA_DIA
    FROM TB_TWEETS
    GROUP BY DATEPART(HOUR,HORARIO)
    ORDER BY QTD_TWEET DESC
"""

# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()

# Converter lista de registros em um Dataframe:
dfHora = pd.DataFrame.from_records(return_query_link,columns=['Quantidade_Tweet','Hora_Dia'])

# Imprime a quantidade de Tweets referente as horas do dia:
print('\nLista das *horas* com maior número de postagens:')
print(dfHora)

# ----------------------------------------------------------------------------------------------
# Fecha conexão com o banco de dados:
cursor.close()
conn.close()
