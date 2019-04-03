
-------------------------------------------------------------------
-- 	Step 1 : Script Criação da Base de Dados SQL  
USE [master]
GO

CREATE DATABASE DB_TELEMEDICINA
GO

-------------------------------------------------------------------
-- Step 2 : Criação de Usuário e permissões de acesso ao Banco

CREATE LOGIN [adm] WITH 
	PASSWORD='admin', 
	DEFAULT_DATABASE=[master], 
	DEFAULT_LANGUAGE=[us_english], 
	CHECK_EXPIRATION=ON, CHECK_POLICY=ON
GO

ALTER SERVER ROLE [sysadmin] ADD MEMBER [adm] 
GO

ALTER SERVER ROLE [serveradmin] ADD MEMBER [adm]
GO

ALTER SERVER ROLE [dbcreator] ADD MEMBER [adm]
GO

ALTER SERVER ROLE [bulkadmin] ADD MEMBER [adm]
GO

-------------------------------------------------------------------
-- Step 3 : Criação das Tabelas

USE [DB_TELEMEDICINA]
GO

-- Tabela para receber os dados extraidos das URLs:
CREATE TABLE [dbo].[TB_URL_TELEMEDICINA](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[INDICE_GOOGLE] [int] NOT NULL,
	[URL] [varchar](max) NULL,
	[DOMINIO] [varchar](max) NULL,
	[CONTEUDO] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

-- Tabela para receber os dados extraídos dos Tweets: 
CREATE TABLE [dbo].[TB_TWEETS](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[USUARIO] [varchar](max) NULL,
	[DATA] [date] NULL,
	[HORARIO] [time](7) NULL,
	[POSTAGEM] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO