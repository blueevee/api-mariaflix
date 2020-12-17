from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS user_episode (
	id_episode integer REFERENCES episodes (id_episode) NOT NULL,
	id_user integer REFERENCES mariaflix_user (id_user) NOT NULL,
	watched_date date NOT NULL,
    PRIMARY KEY(id_episode, id_user)
);"""
    )


def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_user_episode.csv"):
    
    db.query(f"""
    COPY user_episode
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )


def insertUserEpisode(user_episode):

    return db.insert("user_episode", 
        id_episode=user_episode['id_episode'],
        id_user=user_episode['id_user'],
        watched_date=user_episode['watched_date']
    )



def getUserEpisode():
    query = db.query("select * from user_episode")
    return query


def getUserEpisodeById(id_user, id_episode):

    query = db.query(f"select * from user_episode WHERE id_episode = %s AND id_user = %s" %(id_episode, id_user))
    return query

def getUserEpisodesByUser(id_user):

    query = db.query(f"select * from user_episode WHERE id_user = %s" %(id_user))
    return query


def deleteUserEpisode(id_user, id_episode):

    query = db.query(f"DELETE FROM user_episode WHERE id_episode = %s AND id_user = %s" %(id_episode, id_user))
    return query
    
def editUserEpisode(id_user, id_episode, column, value):

    attributes = db.get_attnames('user_episode')
    if column in attributes:
        db.query(f"UPDATE user_episode SET %s = '%s' WHERE id_user = %s AND id_episode =%s" %(column, value, id_user, id_episode ))
        query = db.query(f"SELECT * FROM  user_episode WHERE id_user = %s AND id_episode = %s" %(id_user, id_episode))
        return query
    else:
        return {"msg":"Essa coluna não foi encontrada"}
