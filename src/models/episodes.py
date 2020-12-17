from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS episodes (
    id_episode serial PRIMARY KEY,
    episode_name   varchar(100) NOT NULL,
    episode_number   integer NOT NULL,
	id_season integer REFERENCES seasons (id_season) NOT NULL
);"""
    )

def restartSequence():
    query = db.query("ALTER SEQUENCE episodes_id_episode_seq RESTART WITH 79;")
    return query.dictresult() if query else{"msg":"Não foi possível restartar a sequence"}

def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_episodes.csv"):
    
    db.query(f"""
    COPY episodes
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )

def insertEpisode(episode):
    return db.insert("episodes", 
        episode_name=episode['episode_name'],
        episode_number=episode['episode_number'],
        id_season=episode['id_season']
    )

def getEpisodes():
    query = db.query("select * from episodes")
    return query

def getEpisodeById(id):
    query = db.get('episodes', id)
    return query 

def deleteEpisode(id):
 
    query = db.query(f"DELETE FROM episodes WHERE id_episode = %s" %(id))
    return query
    
def editEpisode(id, column, value):
    attributes = db.get_attnames('episodes')
    if column in attributes:
        db.query(f"UPDATE episodes SET %s = '%s' WHERE id_episode = %s" %(column, value, id))
        query = db.query(f"SELECT * FROM episodes WHERE id_episode =%s"%(id))
        return query
    else:
        return {"msg":"Essa coluna não foi encontrada"}
