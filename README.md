# Primera Api con Python🐍 utilizando Flask


## Herramientas Utilizadas🛠️

### Backend
 Python, Flask, Flask-MySQLdb, mysqlclient

###### Crear Entorno Virtual virtualenv -p python3 env
Para activarlo .\env\Scrits\activate 

###### Para ejecutarlo de forma local desde el backend:
## python .\src\app.py



#### Backend coneccion a base de datos MYSQL, crea un archivo config.py

class DevelopmentConfig():
   ##### DEBUG= True
   ##### MYSQL_HOST = 'tu_localHost'
   ##### MYSQL_USER = 'tu_User'
   ##### MYSQL_PASSWORD = 'tu_clave'
   ##### MYSQL_DB = 'escoge_un_nombre'
   ##### MYSQL_PORT = 3306
    

config = {
    'development': DevelopmentConfig
}

# - Nicolas Viruel🐤
