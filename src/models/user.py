from db.connection import db
from pg import DatabaseError, IntegrityError


def createTable():
    db.query("""
    CREATE TABLE IF NOT EXISTS mariaflix_user (
    id_user serial PRIMARY KEY,
    mariaflix_user_name   varchar(200) NOT NULL,
	email varchar(100) NOT NULL UNIQUE,
	cpf char(11) NOT NULL UNIQUE,
	cellphone char(11) NOT NULL
);"""
    )

def populateTable(csv_file=r"C:\Users\evelyn.ferreira\Desktop\eevee\estudos\python\SERASA\api-mariaflix\src\sample\payload_user.csv"):
    
    db.query(f"""
    COPY mariaflix_user
    FROM '{csv_file}'
    WITH DELIMITER AS ',' CSV;
    """
    )

def restartSequence():
    query = db.query("ALTER SEQUENCE mariaflix_user_id_user_seq RESTART WITH 21;")
    return query.dictresult() if query else{"msg":"Não foi possível restartar a sequence"}

def insertUser(mariaflix_user):
    
    return db.insert("mariaflix_user", 
        mariaflix_user_name= mariaflix_user['mariaflix_user_name'],
        email= mariaflix_user['email'],
        cpf= mariaflix_user['cpf'],
        cellphone= mariaflix_user['cellphone']
    )

def getUser():
    query = db.query("select * from mariaflix_user")
    return query

def getUserById(id):
    
    query = db.get('mariaflix_user', id)
    return query

def deleteUser(id):

    query = db.query(f"DELETE FROM mariaflix_user WHERE id_user = %s" %(id))
    return query
    
def editUser(id, column, value):

    attributes = db.get_attnames('mariaflix_user')
    if column in attributes:
        db.query(f"UPDATE mariaflix_user SET %s = '%s' WHERE id_user = %s" %(column, value, id))
        query = db.query(f"SELECT * FROM mariaflix_user WHERE id_user =%s"%(id))
        return query.dictresult() if query else {"msg":"Não foram encontrados registros"}, 404
    else:
        return {"msg":"Essa coluna não foi encontrada"}, 404