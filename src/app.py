from flask import Flask, jsonify, request
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
        cursos = []
        for fila in datos:
            # para convertirlos en json
            # accedemos mediante el indice correspondiente que devuelve el print de datos, ya que estan dentro de tuplas.
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)

        return jsonify({'cursos': cursos, 'mensaje': "Cursos Listados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


# Leer un solo curso
@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT Codigo, Nombre, Creditos FROM flask_cursos.cursos WHERE codigo= '{0}'".format(
            codigo)  # le paso como parametro el codigo que necesito buscar
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0],
                     'nombre': datos[1], 'creditos': datos[2]}
            # respuesta el curso
            return jsonify({'curso': curso, 'mensaje': "Curso Encontrado"})
        else:
            return jsonify({'message': "Curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
# Error de Pagina


def pagina_no_encontrada(error):
    return "<h1>La pagina que intentas buscar no existe</h1>",

# Crear un Curso
@app.route('/cursos', methods=['POST'])
def registrar_curso():

    try:
        # Validación de datos
        if not all(key in request.json for key in ('codigo', 'nombre', 'creditos')):
            return jsonify({'mensaje': "Faltan datos"}), 400

        codigo = request.json['codigo']
        nombre = request.json['nombre']
        creditos = request.json['creditos']

        cursor = conexion.connection.cursor()

        # Verificar si el código ya existe
        sql_check = "SELECT COUNT(*) FROM flask_cursos.cursos WHERE codigo = %s"
        cursor.execute(sql_check, (codigo,))
        (count,) = cursor.fetchone()

        if count > 0:
            return jsonify({'mensaje': "El código ya existe"}), 409  # Devuelve 409 para conflicto de un codigo ya existente


        sql = """INSERT INTO flask_cursos.cursos (codigo, nombre, creditos) VALUES (%s, %s, %s)"""
        # Utilizar parámetros para evitar inyección SQL
        cursor.execute(sql, (codigo, nombre, creditos))
        conexion.connection.commit()  # confirma la acción de insertar el código

        # Devuelve 201 para indicar creación exitosa
        return jsonify({'message': "Curso registrado"}), 201

    except Exception as ex:
        # print("Error:", ex)
        return jsonify({'mensaje': "Error"}), 500

#Actualizar Curso
@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        # Validación de datos
        if not all(key in request.json for key in ('nombre', 'creditos')):
            return jsonify({'mensaje': "Faltan datos"}), 400

        nombre = request.json['nombre']
        creditos = request.json['creditos']

        cursor = conexion.connection.cursor()

        # Verificar si el curso existe
        sql_check = "SELECT COUNT(*) FROM flask_cursos.cursos WHERE codigo = %s"
        cursor.execute(sql_check, (codigo,))
        (count,) = cursor.fetchone()

        if count == 0:
            return jsonify({'mensaje': "Curso no encontrado."}), 404

        # Si el curso existe, actualiza los datos
        sql_update = """UPDATE flask_cursos.cursos SET nombre = %s, creditos = %s WHERE codigo = %s"""
        cursor.execute(sql_update, (nombre, creditos, codigo))
        conexion.connection.commit()

        return jsonify({'mensaje': "Curso actualizado."}), 200

    except Exception as ex:
        print("Error:", ex)
        return jsonify({'mensaje': "Error"}), 500    


#Eliminar Curso
@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM flask_cursos.cursos WHERE codigo = %s"
        cursor.execute(sql, (codigo,))
        conexion.connection.commit()

        # Comprobar si alguna fila fue afectada
        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Curso eliminado."}), 200
        else:
            return jsonify({'mensaje': "Curso no encontrado."}), 404

        return jsonify({'message: "Curso eliminado.'})

    except Exception as ex:
        print("Error:", ex)
        return jsonify({'mensaje': "Error"})


if __name__ == '__main__':
    app.config.from_object(config['development'])
    # Le agrego el codigo de respuesta 404
    app.register_error_handler(404, pagina_no_encontrada), 404
    app.run(port=5001)
