# alfred-on-docker
Após baixar o projeto, acesse a pasta principal. Uma vez acessada, basta rodar os seguintes comandos:

    docker-compose up -d
Quando o docker terminar de montar tudo, acessamos a aplicação:

    docker-compose run app bash
 Agora que estamos na aplicação temos que rodar um comandinho para levantar o projeto.
 

    python project_up.py
Pronto! O projeto já está rodando! Para começar a lançar as notas, temos que rodar um outro comando. Neste caso, sempre que você for lançar, tem que rodar esse comandinho ^^

    python main.py
