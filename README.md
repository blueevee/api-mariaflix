[get-image]: https://img.shields.io/badge/-GET-green
[post-image]: https://img.shields.io/badge/-POST-yellow
[del-image]: https://img.shields.io/badge/-DELETE-critical
[py-image]: https://img.shields.io/badge/Python-v3.7.4-success
[pygree-image]: https://img.shields.io/badge/PyGreSQL-v5.2.1-blue
[psql-image]: https://img.shields.io/badge/PostgreSQL-v13.0-blue
[flask-image]: https://img.shields.io/badge/Flask_RESTful-v0.3.8-blue
[py-url]: https://www.python.org/
[pygree-url]: https://pypi.org/project/PyGreSQL/
[flask-url]: https://pypi.org/project/Flask-RESTful/
[psql-url]: https://www.postgresql.org/
# PROJETO FINAL MVCAD 2020

## PROPOSTA
### MariaFlix
>Estamos desenvolvendo um projeto pra criar o MariaFlix, uma plataforma onde teremos um catálogo de filmes e séries dos mais diversos. Para isso, precisamos atender as seguintes funcionalidades.

- Ter um CRUD de filmes e séries.
- Ter um CRUD de usuários.
- Endpoint para associar o usuário à um filme ou episódio de uma série.
- Relatório para verificar todos os filmes que uma pessoa viu.
- Relatório para verificar todos as temporadas inteiras de uma série que uma pessoa viu.
- Relatório para verificar quem foram as TOP5 pessoas que mais assistiram algo dentro do MariaFlix em um determinado mês.

> O projeto tem como escopo fazer uma api usando python, flask e postgreSQL.  
[![Python Version][py-image]][py-url]
[![Flask version][flask-image]][flask-url]
[![Postgres version][psql-image]][psql-url]
[![Pygree version][pygree-image]][pygree-url]

## TASKLIST

- [X] Ter um CRUD de filmes e séries.
- [X] Ter um CRUD de usuários.
- [X] Endpoint para associar o usuário à um filme ou episódio de uma série.
- [X] Relatório para verificar todos os filmes que uma pessoa viu.
- [X] Relatório para verificar todos as temporadas inteiras de uma série que uma pessoa viu.
- [X] Relatório para verificar quem foram as TOP5 pessoas que mais assistiram algo dentro do MariaFlix em um determinado mês.
- [X] Relatório para verificar as TOP5 series mais assistidas dentro do MariaFlix em um determinado mês.
- [X] Relatório para verificar os TOP5 filmes mais assistidas dentro do MariaFlix em um determinado mês.
- [ ] Refatorar carga de dados nas tabelas.
- [ ] Refatorar função do relátorio de top 5 pessoas que mais asitiram algo 
- [ ] Fazer documentação com swagger api  

## RODANDO O PROJETO
---

1. Com o python instalado faça o clone do repositório

2. Caso não tenha uma virtualenv, instale com: `pip install virtualenv`
        
    2.1 Depois crie a virtualenv : `virtualenv venv`

    2.2 E ative com: 
> OS X & Linux
```sh
source venv/bin/activate
```
> Windows:
```sh
source venv/Scripts/activate
```
3. Com a virtualenv ativa, instale rode: `pip install -r requirements.txt`

4. Preecha no arquivo [connection.example.py](https://github.com/blueevee/api-mariaflix/blob/main/src/db/connection.example.py) suas configurações do banco de dados.

5. Rode o arquivo [init.py](https://github.com/blueevee/api-mariaflix/blob/main/src/init.py) para criar e popular as tabelas: `python src/init.py`

6. Rode o arquivo [api.py](https://github.com/blueevee/api-mariaflix/blob/main/src/api.py) para iniciar o servidor e testar os endpoints: `python src/api.py`


# Endpoints  



## __Usuários__
***
### ![GET][get-image] */user*
> Retorna todos os usuários
### ![GET][get-image] */user/:id*
> Retorna o usuário do id informado  

>**Ex:** */user/3*
 ```json
 { 
    "id_user": 3, 
    "mariaflix_user_name": "Alini",
    "email": "a.lini@kawaii.doll.br",
    "cpf": "27185602157",
    "cellphone": "8427802846 "
}
```
### ![POST][post-image] */user*
> Insere um novo usuário  
 ```json
 {  
    "mariaflix_user_name": "Priscila Power",
    "email": "pri@queen.power.com",
    "cpf": "22321261901",
    "cellphone": "1239252772 "
}
```
### ![POST][post-image] */user/:id*
> Edita 1 atributo de 1 usuário  

>**Ex:** */user/3*
 ```json
 { 
    "column": "mariaflix_user_name",
    "value": "Alini Ribeiro"
}
```
### ![DEL][del-image] */user/:id*
> Exclui 1 usuário da base

## __Gêneros__
***
### ![GET][get-image] */gender*
> Retorna todos os gêneros cadastrados
### ![GET][get-image] */gender/:id*
> Retorna o gênero do id informado  

>**Ex:** */gender/5*
 ```json
 {
    "id_gender": 5,
    "gender_name": "Documentário"
}
```
### ![POST][post-image] */gender*
> Insere um novo gênero  
 ```json
 {
    "gender_name": "Animação"
}
```
### ![POST][post-image] */gender/:id*
> Edita 1 atributo de 1 gênero  

>**Ex:** */user/3*
 ```json
 { 
    "column": "gender_name",
    "value": "Terror"
}
```
### ![DEL][del-image] */gender/:id*
> Exclui 1 gênero da base

## __Filmes__
***
### ![GET][get-image] */films*
> Retorna todos os filmes cadastrados
### ![GET][get-image] */films/:id*
> Retorna o filme do id informado  

>**Ex:** */films/19*
 ```json
{
    "id_film": 19,
    "film_name": "O Império Contra-ataca",
    "duration": "02:07:00",
    "release_year": "1980",
    "gender_name": "Ficção científica"
    }
```
### ![POST][post-image] */films*
> Insere um novo filme  
 ```json
{
    "film_name": "Beleza Oculta",
    "duration": "01:37:00",
    "release_year": "2016",
    "id_gender": 1
}
```
### ![POST][post-image] */films/:id*
> Edita 1 atributo de 1 filme  

>**Ex:** */user/22*
 ```json
 { 
    "column": "id_gender",
    "value": 14
}
```
### ![DEL][del-image] */films/:id*
> Exclui 1 filme da base

## __Series__
***
### ![GET][get-image] */series*
> Retorna todos os seriados cadastrados
### ![GET][get-image] */series/:id*
> Retorna o seriado do id informado  

>**Ex:** */series/3*
 ```json
{
    "id_serie": 3,
    "serie_name": "Biohackers",
    "seasons_quantity": 1,
    "gender_name": "Ficção científica"
    }
```
### ![POST][post-image] */series*
> Insere um novo seriado  
 ```json
{
    "serie_name": "Demon Slayer",
    "seasons_quantity": 2,
    "id_gender": 2
}
```
### ![POST][post-image] */series/:id*
> Edita 1 atributo de 1 seriado  

>**Ex:** */series/5*
 ```json
 { 
    "column": "seasons_quantity",
    "value": 1
}
```
### ![DEL][del-image] */series/:id*
> Exclui 1 seriado da base

## __Temporadas__
***
### ![GET][get-image] */seasons*
> Retorna todas as temporadas cadastradas
### ![GET][get-image] */seasons/:id*
> Retorna a temporada do id informado  

>**Ex:** */seasons/2*
 ```json
{
    "id_season": 2,
    "season_number": 2,
    "episodes_quantity": 8,
    "serie_name": "Sex Education"
    }
```
### ![POST][post-image] */seasons*
> Insere uma nova temporada  
 ```json
{  
    "season_number": 3,
    "episodes_quantity": 8,
    "id_serie": 1
}
```
### ![POST][post-image] */seasons/:id*
> Edita 1 atributo de 1 temporada  

>**Ex:** */seasons/5*
 ```json
 { 
    "column": "episodes_quantity",
    "value": 10s
}
```
### ![DEL][del-image] */seasons/:id*
> Exclui 1 temporada da base

## __Episódios__
***
### ![GET][get-image] */episodes*
> Retorna todos os episódios cadastrados   

### ![GET][get-image] */episodes/:id*
> Retorna o episódio do id informado  

>**Ex:** */episodes/55*
 ```json
{
    "id_episode": 55,
    "episode_name": "Suspicion",
    "episode_number": 3,
    "id_season": 7
    }
```
### ![POST][post-image] */episodes*
> Insere um novo episódio  
 ```json
{
    "episode_name": "Pilot",
    "episode_number": 1,
    "id_season": 1
}
```
### ![POST][post-image] */episodes/:id*
> Edita 1 atributo de 1 episódio  

>**Ex:** */episodes/78*
 ```json
 { 
    "column": "episode_number",
    "value": 10
}
```
### ![DEL][del-image] */episodes/:id*
> Exclui 1 episódio da base

## __Usuário para episódio__
***
### ![GET][get-image] */userEpisode*
> Retorna todos os episódios associados aos usuários    

### ![GET][get-image] */userEpisode/:id_user*
> Retorna todos os episódios associados ao usuário informado

### ![GET][get-image] */userEpisode/:id_user/:id_episode*
> Retorna o episódio associado ao usuário dos ids informados  

>**Ex:** */userEpisode/3/66*
 ```json
{
    "id_episode": 66,
    "id_user": 3,
    "watched_date": "2020-04-10"
}
```
### ![POST][post-image] */userEpisode*
> Insere um novo episódio  
 ```json
{
    "id_episode": 77,
    "id_user": 3,
    "watched_date": "2020-04-10"
}
```
### ![POST][post-image] */userEpisode/:id_user/:id_episode*
> Edita 1 atributo de 1 usuário associado ao episódio  

>**Ex:** */userEpisode/3/78*
 ```json
 { 
    "column": "watched_date",
    "value": "2020-04-10"
}
```
### ![DEL][del-image] */userEpisode/:id_user/:id_episode*
> Exclui 1 usuário associado ao episódio

## __Usuário para filme__
***
### ![GET][get-image] */userFilm*
> Retorna todos os filmes associados aos usuários    

### ![GET][get-image] */userFilm/:id_film*
> Retorna todos os filmes associados ao usuário informado

### ![GET][get-image] */userFilm/:id_user/:id_film*
> Retorna o filme associado ao usuário dos ids informados  

>**Ex:** */userFilm/8/1*
 ```json
{
    "id_film": 1,
    "id_user": 8,
    "watched_date": "2020-04-02"
}
```
### ![POST][post-image] */userFilm*
> Insere um novo filme  
 ```json
{
    "id_film": 5,
    "id_user": 3,
    "watched_date": "2020-10-10"
}
```
### ![POST][post-image] */userFilm/:id_user/:id_film*
> Edita 1 atributo de 1 usuário associado ao filme  

>**Ex:** */userFilm/3/5*
 ```json
 { 
    "column": "watched_date",
    "value": "2020-06-12"
}
```
### ![DEL][del-image] */userFilm/:id_user/:id_film*
> Exclui 1 usuário associado ao filme

## __Filmes assitidos__
***
### ![GET][get-image] */allWatchedFilms/:id*
> Retorna todos os filmes assistidos pelo usuário com detalhes    

## __Temporadas assitidas__
***
### ![GET][get-image] */allWatchedSeries/:id*
> Retorna todas as temporadas completas assistidos pelo usuário informado    

## __TOP 5__
***
### ![GET][get-image] */topFiveByAny/:id*
> Retorna o top 5 de usuários que mais assistiram algo no mês informado   

## __TOP 5 - por filmes__
***
### ![GET][get-image] */topFiveByFilms/:month*
> Retorna o top 5 de usuários que assistiram mais filmes no mês informado  
> **Valores que podem ser usados em month:**
```py
[01 , 02, 03 , 04 , 05, 06 , 07 , 08 , 09 , 10 , 11 , 12]
```   

## __TOP 5 - por séries__
***
### ![GET][get-image] */topFiveBySeries/:month*
> Retorna o top 5 de usuários que assistiram mais séries no mês informado  
> **Valores que podem ser usados em month:**
```py
[01 , 02, 03 , 04 , 05, 06 , 07 , 08 , 09 , 10 , 11 , 12]
```   

## __TOP 5 filmes__
***
### ![GET][get-image] */topFiveWatchedFilms/:month*
> Retorna o top 5 de filmes mais assistidos no mês informado  
> **Valores que podem ser usados em month:**
```py
[01 , 02, 03 , 04 , 05, 06 , 07 , 08 , 09 , 10 , 11 , 12]
```   

## __TOP 5 séries__
***
### ![GET][get-image] */topFiveWatchedSeries/:month*
> Retorna o top 5 de séries mais assistidas no mês informado  
> **Valores que podem ser usados em month:**
```py
[01 , 02, 03 , 04 , 05, 06 , 07 , 08 , 09 , 10 , 11 , 12]
```   
