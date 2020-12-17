from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS series (
    id_serie serial PRIMARY KEY,
    serie_name   varchar(100) NOT NULL,
	seasons_quantity integer NOT NULL,
	id_gender integer REFERENCES gender (id_gender) NOT NULL
);"""
    )

def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_series.csv"):
    
    db.query(f"""
    COPY series
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )

def restartSequence():
    query = db.query("ALTER SEQUENCE series_id_serie_seq RESTART WITH 5")
    return query.dictresult() if query else{"msg":"Não foi possível restartar a sequence"}

def insertSerie(serie):
         
    return db.insert("series", 
        serie_name=serie['serie_name'],
        seasons_quantity=serie['seasons_quantity'],
        id_gender=serie['id_gender']
    )

def getSeries():
    query = db.query("""SELECT s.id_serie,s.serie_name,s.seasons_quantity, g.gender_name
                        FROM series as s
                        INNER JOIN gender as g ON (s.id_gender = g.id_gender)""")
    return query

def getSerieById(id):

    query = db.get('series', id)
    return query 

def deleteSerie(id):

    query = db.query(f"DELETE FROM series WHERE id_serie = %s" %(id))
    return query
    
def editSerie(id, column, value):

    attributes = db.get_attnames('series')
    if column in attributes:
        db.query(f"UPDATE series SET %s = '%s' WHERE id_serie = %s" %(column, value, id))
        query = db.query(f"SELECT * FROM series WHERE id_serie =%s"%(id))
        return query.dictresult() if query else {"msg":"Não foram encontrados registros"}
    else:
        return {"msg":"Essa coluna não foi encontrada"}
