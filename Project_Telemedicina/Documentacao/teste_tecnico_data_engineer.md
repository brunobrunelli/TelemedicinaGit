# Desafio - Data Engineer



### Proposta

Implementar uma aplicação para realização de web scraping, execução de REST APIs públicas e manipulação e consulta de banco de dados (usando SQL).



### Requisitos



* A aplicação deve ser desenvolvida inteiramente usando a linguagem Python;

* Esse teste deve ser entregue em no máximo 10 (dez) dias úteis após o recebimento do mesmo, ou o candidato será desclassificado;

* A aplicação deve consultar o termo "telemedicina" no Google e armazenar em um banco de dados local os 100 primeiros resultados (posição de ordenação pelo Google, endereço completo do site de origem e conteúdo completo da página de resultado);

* A aplicação deve utilizar a REST API pública do Twitter e armazenar no mesmo banco de dados local as últimas 1000 postagens contendo o termo "telemedicina" (usuário, data e hora da postagem e conteúdo);

* A aplicação deve consultar o banco de dados local e demonstrar:

1) Dos 100 primeiros resultados armazenados no banco de dados, retornar a lista ordenada de domínios mais frequentes (por exemplo, para o endereço portaltelemedicina.com.br/telemedicina-o-que-e-e-como-funciona/ o domínio seria portaltelemedicina.com.br);

2) Considerando os conteúdos completos das páginas de resultado, montar uma lista com os 100 termos (palavras chave) mais utilizados (ignorar palavras não relacionadas à telemedicina, como por exemplo: de, não, por, a, o, etc.);

3) Lista de usuários do twitter com maior número de postagens com o termo telemedicina;

4) Em qual dia da semana são feitas mais postagens com o termo telemedicina;

5) Em qual hora do dia são feitas mais postagens com o termo telemedicina;



### Definição de Pronto



* A aplicação deve rodar após clonarmos o repositório localmente e executarmos o build  (por exemplo, criar um ambiente virtual (usando virtualenv) e executar `pip install -r requirements.txt`);

* Adicionar um arquivo README.md com instruções de como executar a aplicação;

* Utilize o banco de dados que preferir (relacional ou noSQL). Recomendamos SQLServer ou MongoDB;



### Observações



* Preze pela simplicidade e resolução do problema com objetividade;

* Opte por ferramentas de terceiros apenas quando julgar estritamente necessário;

* Cuidado com a organização e estrutura do projeto;

* Documentação é sempre bem-vinda; 

* Certifique-se que o projeto segue boas práticas de desenvolvimento, incluindo segurança e otimização;

* Use corretamente o controle de versão (Git). Principalmente os commits realizados na construção do projeto. Não tenha medo de realizar commits realmente atômicos (gostaríamos de entender todo o seu processo de pensamento na construção do projeto);
* Ferramentas visuais (como gráficos) para apresentação dos resultados contarão pontos extras;




### Processo de submissão

* O desafio deve ser entregue pelo [GitHub](http://github.com/), [Bitbucket](http://bitbucket.org/) ou [GitLab](http://gitlab.com/). Envie a  URL por e-mail.
* Qualquer dúvida em relação ao desafio, responderemos por e-mail.

Bom trabalho!