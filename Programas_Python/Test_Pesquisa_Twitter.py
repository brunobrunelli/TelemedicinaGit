#!/usr/bin/env python
# coding: utf-8

# 1 - Leitura e Gravação dos dados no Banco SQL - Pesquisa Tweet:

# In[200]:


# Imports:
from twython import Twython
import json
import pandas as pd
import time
import pyodbc 


# In[201]:


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


# In[202]:


# Extraindo as credenciais de acesso de um arquivo .json:
with open("twitter_credentials.json", "r") as file:  
    creds = json.load(file)


# In[203]:


# Instanciando um objeto twython:
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])


# In[204]:


# Criando query com os parametros a serem passados no método:
#query = {'q': 'telemedicina','count': 100000,'lang': 'pt'}
query = {'q': 'telemedicina','lang': 'pt'}


# In[205]:


# Dicionário para armazenar os tweets:
dict_twitter = {'usuario': [], 'data': [], 'horario':[], 'postagem': []}


# In[206]:


lista_twitter = []


# In[207]:


maximo = 0
id_inicio = 0
i = 0


# In[208]:


for status in python_tweets.search(q='telemedicina',count=100,since_id=id_inicio,lang='pt')['statuses']:  
    id_user = (status['id'])
    usuario = (status['user']['screen_name'])
    data = (time.strftime('%Y-%m-%d', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
    horario = (time.strftime('%H:%M:%S', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
    postagem = (status['text'])

    values = [usuario, data, horario, postagem]
    lista_twitter.append(values)

    i += 1
    
    # Ira receber sempre o maior id:
    if id_user > maximo:
        maximo = id_user
        print('id Max - ' + str(maximo))


# In[209]:


print(maximo)


# In[210]:


id_inicio = maximo


# In[211]:


id_inicio+1


# In[212]:


for status in python_tweets.search(q='telemedicina',count=100,since_id=id_inicio,lang='pt')['statuses']:  
    id = (status['id'])
    usuario = (status['user']['screen_name'])
    data = (time.strftime('%Y-%m-%d', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
    horario = (time.strftime('%H:%M:%S', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
    postagem = (status['text'])

    values = [usuario, data, horario, postagem]
    lista_twitter.append(values)

    i += 1
        
    # Ira receber sempre o maior id:
    if id > maximo:
        maximo = id
        print('id Max - ' + str(maximo))


# In[214]:


print(i)


# In[213]:


print(len(lista_twitter))

conn.close()

