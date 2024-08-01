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