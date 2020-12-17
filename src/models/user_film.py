from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS user_film (
	id_film integer REFERENCES films (id_film) NOT NULL,
	id_user integer REFERENCES mariaflix_user (id_user) NOT NULL,
	watched_date date NOT NULL,
    PRIMARY KEY(id_film, id_user)
);"""
    )


def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_user_film.csv"):
    
    db.query(f"""
    COPY user_film
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )


def insertUserFilm(user_film):

    return db.insert("user_film", 
    id_film=user_film['id_film'],
    id_user=user_film['id_user'],
    watched_date=user_film['watched_date']
    )


def getUserFilm():
    query = db.query("select * from user_film")
    return query

def getUserFilmsByUser(id_user):

    query = db.query(f"select * from user_film WHERE id_user = %s" %(id_user))
    return query


def getUserFilmById(id_user,id_film):

    query = db.query(f"select * from user_film WHERE id_film = %s AND id_user = %s" %(id_film, id_user))
    return query

def deleteUserFilm(id_user,id_film):
    
        query = db.query(f"DELETE FROM user_film WHERE id_film = %s AND id_user = %s" %(id_film, id_user))
        return query
    
def editUserFilm(id_user,id_film, column, value):
 
    attributes = db.get_attnames('user_film')
    if column in attributes:
        db.query(f"UPDATE user_film SET %s = '%s' WHERE id_film = %s AND id_user =%s" %(column, value, id_film, id_user))
        query = db.query(f"SELECT * FROM  user_film WHERE id_film = %s AND id_user = %s"%(id_film, id_user))
        return query
    else:
        return {"msg":"Essa coluna não foi encontrada"}
  