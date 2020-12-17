from db.connection import db
from pg import DatabaseError, IntegrityError


def getAllWatchedSeasons(id_user):
    query = db.query("""SELECT count(*), se.serie_name, s.season_number as season, s.episodes_quantity
        FROM user_episode as ue INNER JOIN episodes as e ON (ue.id_episode = e.id_episode) 
        INNER JOIN seasons as s ON (s.id_season = e.id_season)
        INNER JOIN series as se ON (s.id_serie = se.id_serie)
        WHERE id_user = %s
        GROUP BY se.serie_name, s.id_season""" % (id_user))
    complete_seasons = lambda o: o['count'] == o['episodes_quantity']
    seasons = list(filter(complete_seasons, query.dictresult()))
    format_response = lambda o: {'serie_name': o['serie_name'] ,'season': o['season']}
    response = list(map(format_response, seasons))
    return response

def getAllWatchedFilms(id_user):
    query = db.query("""SELECT uf.watched_date,f.id_film, f.film_name, mu.mariaflix_user_name as user
        FROM user_film as uf 
        INNER JOIN films as f ON (f.id_film = uf.id_film) 
        INNER JOIN mariaflix_user as mu ON (mu.id_user = uf.id_user) 
        WHERE uf.id_user = %s""" % (id_user))
    return query

def getAllWatchedFilms(id_user):
    query = db.query("""SELECT uf.watched_date,f.id_film, f.film_name, mu.mariaflix_user_name as user
        FROM user_film as uf 
        INNER JOIN films as f ON (f.id_film = uf.id_film) 
        INNER JOIN mariaflix_user as mu ON (mu.id_user = uf.id_user) 
        WHERE uf.id_user = %s""" % (id_user))
    return query

def getTopFiveBySeries(month):
    query = db.query("""SELECT COUNT(ue.id_user) as eps, mu.mariaflix_user_name as name
        FROM user_episode as ue INNER JOIN mariaflix_user as mu ON (mu.id_user = ue.id_user)
        WHERE watched_date::text LIKE '____-%s-__' 
        GROUP BY ue.id_user, mu.mariaflix_user_name
        ORDER BY COUNT(ue.id_user) DESC LIMIT 5""" % (month))

    format_response = lambda o: {'episodes': o['eps'] ,'user': o['name']}
    response = list(map(format_response, query.dictresult()))
    return response

def getTopFiveByFilms(month):
    query = db.query("""SELECT COUNT(uf.id_user) as films, mu.mariaflix_user_name as name
    FROM user_film as uf INNER JOIN mariaflix_user as mu ON (mu.id_user = uf.id_user)
    WHERE watched_date::text LIKE '____-%s-__' 
    GROUP BY uf.id_user, mu.mariaflix_user_name
    ORDER BY COUNT(uf.id_user) DESC LIMIT 5""" % (month))

    format_response = lambda o: {'films': o['films'] ,'user': o['name']}
    response = list(map(format_response, query.dictresult()))
    return response

def getTopFiveWatchedFilms(month):
    query = db.query("""SELECT COUNT(uf.id_film) as times, f.film_name as title
    FROM user_film as uf INNER JOIN films as f ON (f.id_film = uf.id_film)
    WHERE watched_date::text LIKE '____-%s-__' 
    GROUP BY uf.id_film, f.film_name
    ORDER BY COUNT(uf.id_film) DESC LIMIT 5""" % (month))
    return query.dictresult()

def getTopFiveWatchedSeries(month):
    query = db.query("""SELECT count(*), se.serie_name
    FROM user_episode as ue INNER JOIN episodes as e ON (ue.id_episode = e.id_episode) 
    INNER JOIN seasons as s ON (s.id_season = e.id_season)
    INNER JOIN series as se ON (s.id_serie = se.id_serie)
    WHERE watched_date::text LIKE '____-%s-__' 
    GROUP BY se.serie_name
    ORDER BY COUNT(*) DESC LIMIT 5""" % (month))
    return query.dictresult()



def formatToThings(obj):
    if 'episodes' in obj:
        return obj['episodes']
    if 'films' in obj:
        return obj['films']

def getTopFiveByAny(month):
    series = getTopFiveBySeries(month)
    films = getTopFiveByFilms(month)

    format_response = lambda o: {'things': formatToThings(o) ,'user': o['user']}
    top_five_films = list(map(format_response, films))
    top_five_series = list(map(format_response, series))
 
    top_five_films =  sorted(top_five_films, key=lambda item : item['user'])
    top_five_series =  sorted(top_five_series, key=lambda item : item['user'])
    pop_series = []
    pop_films = []
    top_any =[]
    for s in top_five_series:
        for f in top_five_films:
            if s['user'] == f['user']:
                top_any.append({'things': s['things'] + f['things'] ,'user': s['user']})
                pop_films.append(top_five_films.index(f))
                pop_series.append(top_five_series.index(s))
    
    pop_series.reverse()
    [top_five_series.pop(s) for s in pop_series]
        
    pop_films.reverse()
    [top_five_films.pop(f) for f in pop_films]
    
    for s in top_five_series:
        top_any.append(s)

    for f in top_five_films:
        top_any.append(f)

    top_any = sorted(top_any, key=lambda item : item['things'], reverse=True)

    del(top_any[5:])
    return top_any