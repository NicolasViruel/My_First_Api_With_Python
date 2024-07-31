class DevelopmentConfig():
    DEBUG= True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'pichones1'
    MYSQL_DB = 'flask_cursos'
    MYSQL_PORT = 3306
    

config = {
    'development': DevelopmentConfig
}


# import MySQLdb

# db = MySQLdb.connect(host="localhost", user="root", password="pichones1", db="flask_cursos")
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print(f"Database version : {data}")
# db.close()    