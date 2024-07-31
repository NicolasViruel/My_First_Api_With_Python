from flask import Flask, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

# Inicializamos la conexión MySQL
conexion = MySQL(app)

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        print("Conexión a la base de datos exitosa.")
        sql = "SELECT Codigo, Nombre, Creditos FROM flask_cursos.cursos"
        cursor.execute(sql)
        datos = cursor.fetchall()  # Almacenamos todo el fetch en datos
        print(f"Datos obtenidos: {datos}")
        cursos=[]
        for fila in datos:
            #para convertirlos en json 
            curso= {'codigo': fila[0], 'nombre':fila[1], 'creditos':fila[2]} #accedemos mediante el indice correspondiente que devuelve el print de datos, ya que estan dentro de tuplas.
            cursos.append(curso)

        return jsonify({'cursos':cursos, 'mensaje': "Cursos Listados"})
    except Exception as ex:
            return jsonify({'mensaje': "Error"})


# Leer un solo curso
@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT Codigo, Nombre, Creditos FROM flask_cursos.cursos WHERE codigo= '{0}'".format(codigo)#le paso como parametro el codigo que necesito buscar
        cursor.execute(sql)
        datos= cursor.fetchone()
        if datos != None:
             curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
             return jsonify({'curso':curso, 'mensaje': "Curso Encontrado"}) #respuesta el curso 
        else: 
            return jsonify({'message': "Curso no encontrado"})     
    except Exception as ex:
            return jsonify({'mensaje': "Error"})
# Error de Pagina
def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(port=5001)