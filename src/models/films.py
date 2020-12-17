from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS films (
    id_film serial PRIMARY KEY,
    film_name   varchar(100) NOT NULL,
	duration time NOT NULL,
	release_year char(4) NOT NULL,
	id_gender integer REFERENCES gender (id_gender) NOT NULL
);"""
    )

def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_films.csv"):
    
    db.query(f"""
    COPY films
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )

def restartSequence():
    query = db.query("ALTER SEQUENCE films_id_film_seq RESTART WITH 21;")
    return query.dictresult() if query else{"msg":"Não foi possível restartar a sequence"}

def insertFilm(film):
    return db.insert("films", 
        film_name=film['film_name'],
        duration=film['duration'],
        release_year=film['release_year'],
        id_gender=film['id_gender']
    )

def getFilms():
    query = db.query("""SELECT f.id_film,f.film_name,f.duration, f.release_year, g.gender_name
                        FROM films as f
                        INNER JOIN gender as g ON (f.id_gender = g.id_gender)""")
    return query

def getFilmById(id):
    query = db.get('films', id)
    return query 

def deleteFilm(id):

    query = db.query(f"DELETE FROM films WHERE id_film = %s" %(id))
    return query

def editFilm(id, column, value):
    attributes = db.get_attnames('films')
    if column in attributes:
        db.query(f"UPDATE films SET %s = '%s' WHERE id_film = %s" %(column, value, id))
        query = db.query(f"SELECT * FROM films WHERE id_film =%s"%(id))
        return query.dictresult() if query else {"msg":"Não foram encontrados registros"}
    else:
        return {"msg":"Essa coluna não foi encontrada"}
