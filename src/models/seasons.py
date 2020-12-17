from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS seasons (
    id_season serial PRIMARY KEY,
    season_number   integer NOT NULL,
	episodes_quantity integer NOT NULL,
	id_serie integer REFERENCES series (id_serie) NOT NULL
);"""
    )

def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_seasons.csv"):
    
    db.query(f"""
    COPY seasons
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )

def restartSequence():
    query = db.query("ALTER SEQUENCE seasons_id_season_seq RESTART WITH 10;")
    return query.dictresult() if query else{"msg":"Não foi possível restartar a sequence"}

def insertSeason(season):
    return db.insert("seasons", 
        season_number=season['season_number'],
        episodes_quantity=season['episodes_quantity'],
        id_serie=season['id_serie']
    )

def getSeasons():
    query = db.query("""SELECT ss.id_season, ss.season_number, ss.episodes_quantity, s.serie_name
                        FROM series as s
                        INNER JOIN seasons as ss ON (s.id_serie = ss.id_serie)""")
    return query

def getSeasonById(id):
    query = db.get('seasons', id)
    return query 

def deleteSeason(id):
    query = db.query(f"DELETE FROM seasons WHERE id_season = %s" %(id))
    return query
    
def editSeason(id, column, value):

    attributes = db.get_attnames('seasons')
    if column in attributes:
        db.query(f"UPDATE seasons SET %s = '%s' WHERE id_season = %s" %(column, value, id))
        query = db.query(f"SELECT * FROM seasons WHERE id_season =%s" %(id))
        return query
    else:
        return {"msg":"Essa coluna não foi encontrada"}
