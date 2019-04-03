#!/usr/bin/env python
# coding: utf-8

# 1 - Leitura e Gravação dos dados no Banco SQL - Pesquisa Tweet:

# In[255]:


# Imports:
from twython import Twython
import json
import pandas as pd
import time
import pyodbc 


# In[256]:


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


# In[257]:


# Extraindo as credenciais de acesso de um arquivo .json:
with open("twitter_credentials.json", "r") as file:  
    creds = json.load(file)


# In[258]:


# Instanciando um objeto twython:
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])


# In[259]:


# Criando query com os parametros a serem passados no método:
query = {'q': 'telemedicina','count':100,'lang': 'pt'}


# In[260]:


# Dicionário para armazenar os tweets:
dict_twitter = {'usuario': [], 'data': [], 'horario':[], 'postagem': []}


# In[261]:


lista_twitter = []


# In[262]:


# Pesquisando o termo "telemedicina" e retornando os 1000 tweets: 
for status in python_tweets.search(**query)['statuses']:  
    usuario = (status['user']['screen_name'])
    data = (time.strftime('%Y-%m-%d', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
    horario = (time.strftime('%H:%M:%S', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
    postagem = (status['text'])
    
    values = [usuario, data, horario, postagem]
    lista_twitter.append(values)
    
    cursor.execute(sql_command, usuario, data, horario, postagem)

# Estruturar o dado retornado nos tweets armazenando em um Dataframe:
df = pd.DataFrame(dict_twitter)  
df = df.sort_values(['data','horario'], ascending=False)   
# In[263]:


# Commit dos dados incluídos no banco:
conn.commit()


# -------

# 2 - Leitura e Exibição dos dados do Banco SQL - Pesquisa Tweet:

# In[264]:


# Comando SQL para extrair os dados dos usuários com mais tweets:
sql_command_link = """
    SELECT 
        COUNT(*) AS QTD_TWEET, 
        USUARIO
    FROM [dbo].[TB_TWEETS]
    GROUP BY USUARIO
    ORDER BY QTD_TWEET DESC
"""


# In[265]:


# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()


# In[266]:


# Converter lista de registros em um Dataframe:
dfQtdeTweet = pd.DataFrame.from_records(return_query_link,columns=['Quantidade_Tweet','Usuario'])


# In[267]:


# Imprime o dataFrame referente aos dados de Domínio:
print(dfQtdeTweet.head(20))


# -------

# In[268]:


# Comando SQL para extrair os dados dos usuários com mais tweets:
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


# In[269]:


# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()


# In[270]:


# Converter lista de registros em um Dataframe:
dfDiaSemana = pd.DataFrame.from_records(return_query_link,columns=['Quantidade_Tweet','Dia_Semana'])


# In[271]:


# Imprime o dataFrame:
print(dfDiaSemana)


# -------

# In[272]:


# Comando SQL para extrair os dados dos usuários com mais tweets:
sql_command_link = """
    SELECT 
        COUNT(*) AS QTD_TWEET,
        DATEPART(HOUR,HORARIO) AS HORA_DIA
    FROM TB_TWEETS
    GROUP BY DATEPART(HOUR,HORARIO)
    ORDER BY QTD_TWEET DESC
"""


# In[273]:


# Executa comando SQL_Link:
return_query_link = cursor.execute(sql_command_link).fetchall()


# In[274]:


# Converter lista de registros em um Dataframe:
dfHora = pd.DataFrame.from_records(return_query_link,columns=['Quantidade_Tweet','Hora_Dia'])


# In[275]:


# Imprime o dataFrame:
print(dfHora)


# In[276]:


cursor.close()
conn.close()


# In[ ]:




