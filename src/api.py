from flask import Flask, request
from flask_restful import Resource, Api
from pg import DatabaseError, IntegrityError
from models import user, gender, films ,series, seasons , episodes, user_episode, user_film, reports
import json, decimal, datetime, logging


app = Flask(__name__)
api = Api(app)

class DefaultEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,decimal.Decimal):
            return float(o)

        if isinstance(o, datetime.date):
            return o.__str__()

        if isinstance(o, datetime.time):
            return o.__str__()

        super(DefaultEncoder,self).default(o)


class AllWatchedSeries(Resource):#OK
    def get(self, id_user):
        all_series = reports.getAllWatchedSeasons(id_user)
        if all_series:
            return all_series, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(AllWatchedSeries, "/allWatchedSeries/<int:id_user>")


class AllWatchedFilms(Resource):#OK
    def get(self, id_user):
        all_films = reports.getAllWatchedFilms(id_user)
        if all_films:
            query = all_films.dictresult()
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(AllWatchedFilms, "/allWatchedFilms/<int:id_user>")


class TopFiveBySeries(Resource):#OK
    def get(self, month):
        top_five = reports.getTopFiveBySeries(month)
        if top_five:
            return top_five, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(TopFiveBySeries, "/topFiveBySeries/<string(length=2):month>")


class TopFiveByFilms(Resource):#OK
    def get(self, month):
        top_five = reports.getTopFiveByFilms(month)
        if top_five:
            return top_five, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(TopFiveByFilms, "/topFiveByFilms/<string(length=2):month>")


class TopFiveByAny(Resource):#OK
    def get(self, month):
        top_five = reports.getTopFiveByAny(month)
        if top_five:
            return top_five, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(TopFiveByAny, "/topFiveByAny/<string(length=2):month>")


class TopFiveWatchedFilms(Resource):#OK
    def get(self, month):
        top_five = reports.getTopFiveWatchedFilms(month)
        if top_five:
            return top_five, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(TopFiveWatchedFilms, "/topFiveWatchedFilms/<string(length=2):month>")


class TopFiveWatchedSeries(Resource):#OK
    def get(self, month):
        top_five_series = reports.getTopFiveWatchedSeries(month)
        if top_five_series:
            return top_five_series, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
api.add_resource(TopFiveWatchedSeries, "/topFiveWatchedSeries/<string(length=2):month>")


class User(Resource):#OK
    def get(self):
        all_users = user.getUser()
        if all_users:
            return all_users.dictresult(), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_user = request.json
        try:
           return user.insertUser(new_user), 201
        except (KeyError, TypeError):
            msg = {"msg": "Parâmetros de Usuário inválidos",
                    "dados":{"mariaflix_user_name":"Nome completo do usuário",
                            "email":"Email do usuário",
                            "cpf":"Cpf do usuário",
                            "cellphone":"Telefone do usuário"
                        }
                    }    
            return msg, 400
        except Exception:  
            return logging.exception()

api.add_resource(User, "/user")

class UserById(Resource):#OK
    def get(self, id_user):
        try:
            return user.getUserById(id_user), 200
        except DatabaseError:
            msg = {"msg": "Esse usuário não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()

    def post(self, id_user):#OK
        column = request.json
        try:
            query = user.editUser(id_user, column['column'], column['value'])
            return query
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_user):#OK
        try:
            query = user.deleteUser(id_user)
            if int(query):
                msg = {"msg":"usuário deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse usuário não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Este usuário está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()
api.add_resource(UserById,'/user/<int:id_user>')

class Gender(Resource):#OK
    def get(self):
        all_genders = gender.getGender()
        if all_genders:
            return all_genders.dictresult(), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_gender = request.json
        try:
           return gender.insertGender(new_gender), 201
        except (KeyError, TypeError):
            msg = {"msg": "Parâmetros de Gênero inválidos",
                "dados":{"gender_name":"Nome do Gênero"}
                }  
            return msg, 400
        except Exception:  
            return logging.exception()
api.add_resource(Gender, "/gender")

class GenderById(Resource):
    def get(self, id_gender):#OK
        try:
            return gender.getGenderById(id_gender), 200
        except DatabaseError:
            msg = {"msg": "Esse gênero não foi encontrado"}
            return msg, 404

    def post(self, id_gender):#OK
        column = request.json
        try:
            query = gender.editGender(id_gender, column['column'], column['value'])
            return query
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_gender):#OK
        try:
            query = gender.deleteGender(id_gender)
            if int(query):
                msg = {"msg":"gênero deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse gênero não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Este gênero está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(GenderById,'/gender/<int:id_gender>')


class Series(Resource):#OK
    def get(self):
        all_series =  series.getSeries()
        if all_series:
            query = all_series.dictresult()
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_serie = request.json
        try:
            query = series.insertSerie(new_serie)
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        except (KeyError, TypeError):
        
            msg = {"msg": "Parâmetros da Série inválidos",
                "dados":{"serie_name":"Nome da série",
                        "seasons_quantity":"Quantidade de temporadas",
                        "id_gender":"ID do gênero"
                    }
                }
            return msg, 400
        except Exception:  
            return logging.exception()
            
api.add_resource(Series, "/series")


class SeriesById(Resource):
    def get(self, id_serie):#OK
        try:
            query = series.getSerieById(id_serie)
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        except DatabaseError:
            msg = {"msg": "Esse seriado não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
            

    def post(self, id_serie):#OK
        column = request.json
        try:
            query = series.editSerie(id_serie, column['column'], column['value'])
            return json.loads(json.dumps(query, cls=DefaultEncoder))
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_serie):#OK
        try:
            query = series.deleteSerie(id_serie)
            if int(query):
                msg = {"msg":"seriado deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse seriado não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Este seriado está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(SeriesById,'/series/<int:id_serie>')


class Films(Resource):#OK
    def get(self):
        all_films = films.getFilms()
        if all_films:
            query = all_films.dictresult()
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_film = request.json
        try:
            query = films.insertFilm(new_film)
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        except (KeyError, TypeError):
        
            msg = {"msg": "Parâmetros de filme inválidos",
                    "dados":{"film_name":"Nome do filme",
                        "duration":"Duração do filme",
                        "release_year":"Ano de lançamento",
                        "id_films":"ID do gênero"
                            }
                    }
            return msg, 400
        except Exception:  
            return logging.exception()
            
api.add_resource(Films, "/films")


class FilmsById(Resource):
    def get(self, id_film):#OK
        try:
            query = films.getFilmById(id_film)
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        except DatabaseError:
            msg = {"msg": "Esse filme não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
            

    def post(self, id_film):#OK
        column = request.json
        try:
            query = films.editFilm(id_film, column['column'], column['value'])
            return json.loads(json.dumps(query, cls=DefaultEncoder))
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_film):#OK
        try:
            query = films.deleteFilm(id_film)
            if int(query):
                msg = {"msg":"filme deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse filme não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Este filme está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(FilmsById,'/films/<int:id_film>')


class Seasons(Resource):#OK
    def get(self):
        all_seasons = seasons.getSeasons()
        if all_seasons:
            query = all_seasons.dictresult()
            return query, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_season = request.json
        try:
            query = seasons.insertSeason(new_season)
            return query, 200
        except (KeyError, TypeError):
        
            msg = {"msg": "Parâmetros da Temporada inválidos",
                    "dados":{
                        "season_number":"Número da temporada",
                        "episodes_quantity":"Quantidade de episódios",
                        "id_serie":"ID do série"
                    }
                }
            return msg, 400
        except Exception:  
            return logging.exception()
            
api.add_resource(Seasons, "/seasons")


class SeasonsById(Resource):
    def get(self, id_season):#OK
        try:
            query = seasons.getSeasonById(id_season)
            return query, 200
        except DatabaseError:
            msg = {"msg": "Essa temporada não foi encontrada"}
            return msg, 404
        except Exception:  
            return logging.exception()
            

    def post(self, id_season):#OK
        column = request.json
        try:
            query = seasons.editSeason(id_season, column['column'], column['value'])
            return query.dictresult()
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_season):#OK
        try:
            query = seasons.deleteSeason(id_season)
            if int(query):
                msg = {"msg":"Temporada deletada com sucesso"}
                return msg, 200
            msg = {"msg":"Essa Temporada não foi encontrada na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Essa Temporada está em uso, não pode ser deletada"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(SeasonsById,'/seasons/<int:id_season>')


class Episodes(Resource):#OK
    def get(self):
        all_episodes = episodes.getEpisodes()
        if all_episodes:
            query = all_episodes.dictresult()
            return query, 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_episode = request.json
        try:
            query = episodes.insertEpisode(new_episode)
            return query, 200
        except (KeyError, TypeError):
        
            msg = {"msg": "Parâmetros da episódio inválidos",
                "dados":{"episode_name":"Nome do episódio",
                        "episode_number":"Número do episódio",
                        "duration":"Duração do episódio",
                        "id_season":"ID da temporada"
                    }
                }
            return msg, 400
        except Exception:  
            return logging.exception()
            
api.add_resource(Episodes, "/episodes")


class EpisodesById(Resource):
    def get(self, id_episode):#OK
        try:
            query = episodes.getEpisodeById(id_episode)
            return query, 200
        except DatabaseError:
            msg = {"msg": "Esse episódio não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
            

    def post(self, id_episode):#OK
        column = request.json
        try:
            query = episodes.editEpisode(id_episode, column['column'], column['value'])
            return query.dictresult()
        except (KeyError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_episode):#OK
        try:
            query = episodes. deleteEpisode(id_episode)
            if int(query):
                msg = {"msg":"Episódio deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse episódio não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Esse episódio está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(EpisodesById,'/episodes/<int:id_episode>')


class UserEpisode(Resource):#OK
    def get(self):
        user_episodes = user_episode.getUserEpisode()
        if user_episodes:
            query = user_episodes.dictresult()
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_user_episode = request.json
        try:
            query = user_episode.insertUserEpisode(new_user_episode)
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        except IntegrityError:
            return {"msg":"Esse episódio já foi assitido por esse usuário"}
        except (KeyError, TypeError):
        
            msg = {"msg": "Parâmetros de episódio assistido inválidos",
                "dados":{
                    "id_episode": "ID do episódio assitido",
                    "id_user":"ID do usuário que assistiu",
                    "watched_date":"Data em que o filme foi assistido"
                }
                }
            return msg, 400
        except Exception:  
            return logging.exception()
            
api.add_resource(UserEpisode, "/userEpisode")


class UserEpisodeByUser(Resource):
    def get(self, id_user):#OK
        try:
            query = user_episode.getUserEpisodesByUser(id_user)
            if query:
                return json.loads(json.dumps(query.dictresult(), cls=DefaultEncoder)), 200
            else:
                raise DatabaseError
        except DatabaseError:
            msg = {"msg": "Esse usuário não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
api.add_resource(UserEpisodeByUser, "/userEpisode/<int:id_user>")
            

class UserEpisodeById(Resource):
    def get(self, id_user, id_episode):#OK
        try:
            query = user_episode.getUserEpisodeById(id_user, id_episode)
            if query:
                return json.loads(json.dumps(query.dictresult(), cls=DefaultEncoder)), 200
            else:
                raise DatabaseError
        except DatabaseError:
            msg = {"msg": "Esse episódio assistido pelo usuário não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
            

    def post(self, id_user, id_episode):#OK
        column = request.json
        try:
            query = user_episode.editUserEpisode(id_user, id_episode, column['column'], column['value'])
            return json.loads(json.dumps(query.dictresult(), cls=DefaultEncoder))
        except IntegrityError:
            return {"msg":"Esse episódio já foi assitido por esse usuário"}
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_user, id_episode):#OK
        try:
            query = user_episode.deleteUserEpisode(id_user, id_episode)
            if int(query):
                msg = {"msg":"Episódio assistido pelo usuário deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse episódio assitido pelo usuário não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Esse episódio assitido pelo usuário está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(UserEpisodeById,'/userEpisode/<int:id_user>/<int:id_episode>')


class UserFilm(Resource):#OK
    def get(self):
        user_films = user_film.getUserFilm()
        if user_films:
            query = user_films.dictresult()
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        else:
            msg = {"msg":"Não foram encontrados registros"}
            return msg, 404
            

    def post(self):#OK
        new_user_film = request.json
        try:
            query = user_film.insertUserFilm(new_user_film)
            return json.loads(json.dumps(query, cls=DefaultEncoder)), 200
        except IntegrityError:
            return {"msg":"Esse filme já foi assitido por esse usuário"}
        except (KeyError, TypeError):
        
            msg = {"msg": "Parâmetros de filme assitido inválidos",
                "dados":{
                    "id_film": "ID do filme assitido",
                    "id_user":"ID do usuário que assistiu",
                    "watched_date":"Data em que o filme foi assistido"
                }
                }
            return msg, 400
        except Exception:  
            return logging.exception()
            
api.add_resource(UserFilm, "/userFilm")



class UserFilmByUser(Resource):
    def get(self, id_user):#OK
        try:
            query = user_film.getUserFilmsByUser(id_user)
            if query:
                return json.loads(json.dumps(query.dictresult(), cls=DefaultEncoder)), 200
            else:
                raise DatabaseError
        except DatabaseError:
            msg = {"msg": "Esse usuário não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
api.add_resource(UserFilmByUser, "/userFilm/<int:id_user>")


class UserFilmById(Resource):
    def get(self, id_user, id_film):#OK
        try:
            query = user_film.getUserFilmById(id_user, id_film)
            return json.loads(json.dumps(query.dictresult(), cls=DefaultEncoder)), 200
        except DatabaseError:
            msg = {"msg": "Esse episódio assistido pelo usuário não foi encontrado"}
            return msg, 404
        except Exception:  
            return logging.exception()
            

    def post(self, id_user, id_film):#OK
        column = request.json
        try:
            query = user_film.editUserFilm(id_user, id_film, column['column'], column['value'])
            return json.loads(json.dumps(query.dictresult(), cls=DefaultEncoder))
        except IntegrityError:
            return {"msg":"Esse filme já foi assitido por esse usuário"}
        except (KeyError, TypeError):
            msg = {"msg":"Parâmetros inválidos", 
                        "dados":{
                        "column":"Nome da coluna que deseja alterar",
                        "value":"Valor para ser alterado" 
                    }}
            return msg, 400
        except Exception:  
            return logging.exception()
    
    def delete(self, id_user, id_film):#OK
        try:
            query = user_film.deleteUserFilm(id_user, id_film)
            if int(query):
                msg = {"msg":"Episódio assistido pelo usuário deletado com sucesso"}
                return msg, 200
            msg = {"msg":"Esse episódio assitido pelo usuário não foi encontrado na base"}
            return msg, 404
        except IntegrityError:
            msg = {"msg":"Esse episódio assitido pelo usuário está em uso, não pode ser deletado"}
            return msg, 401
        except Exception:  
            return logging.exception()

api.add_resource(UserFilmById,'/userFilm/<int:id_user>/<int:id_film>')


if __name__ == "__main__":
    app.run(debug=True)