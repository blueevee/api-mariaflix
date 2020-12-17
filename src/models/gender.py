from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS gender (
    id_gender serial PRIMARY KEY,
    gender_name   varchar(100) NOT NULL,
);"""
    )

def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_gender.csv"):
    
    db.query(f"""
    COPY gender
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )

def restartSequence():
    query = db.query("ALTER SEQUENCE gender_id_gender_seq RESTART WITH 16;")
    return query.dictresult() if query else{"msg":"Não foi possível restartar a sequence"}

def insertGender(gender):
    return db.insert("gender", 
        gender_name=gender['gender_name'],
    )

def getGender():
    query = db.query("select * from gender")
    return query

def getGenderById(id):

    query = db.get('gender', id)
    return query 

def deleteGender(id):

    query = db.query(f"DELETE FROM gender WHERE id_gender = %s" %(id))
    return query
    
def editGender(id, column, value):

    attributes = db.get_attnames('gender')
    if column in attributes:
        db.query(f"UPDATE gender SET %s = '%s' WHERE id_gender = %s" %(column, value, id))
        query = db.query(f"SELECT * FROM gender WHERE id_gender =%s"%(id))
        return query.dictresult() if query else {"msg":"Não foram encontrados registros"}, 404
    else:
        return {"msg":"Essa coluna não foi encontrada"}, 404
