from flask import Flask, request, jsonify #Se importa el Framework Flask, la libreria request para las peticiones HTTP, Jsonify nos ayuda a serializar datos a formato json """
from flask_sqlalchemy import SQLAlchemy #Se importa el framework SQLALCHEMY para poder interactar con bases de datos"""

app = Flask(__name__) #Se crea una instancia de la clase Flask llamada app. __name__ es una variable especial que representa el nombre del módulo actual."""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/supportbd' #Se configura la URI de la base de datos y se desactiva el seguimiento de modificaciones."""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #Se crea una instancia de SQLAlchemy llamada db para interactuar con la base de datos."""


class Trabajador(db.Model): #Se define un modelo de datos llamado Trabajador que representa a los trabajadores. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    compleacomulada = db.Column(db.Integer, default=0)

    def __init__(self, name, compleacomulada): #__init__: Método constructor que inicializa las propiedades del trabajador"""
        self.name = name
        self.compleacomulada = compleacomulada

class Support(db.Model): #Se define un modelo de datos llamado Support que representa los soportes.Tiene columnas id, description, complejidad, y trabajador_id.
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    complejidad = db.Column(db.Integer, nullable=False)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajador.id'), nullable=True)

    def __init__(self, description, complejidad, trabajador_id): #__init__: Método constructor que inicializa las propiedades del soporte.
        self.description = description
        self.complejidad = complejidad
        self.trabajador_id = trabajador_id

with app.app_context(): #Dentro de un contexto de aplicación, se ejecuta db.create_all() para crear las tablas en la base de datos. Esto debería hacerse dentro del contexto de la aplicación.
    db.create_all()

@app.route('/assign_support', methods=['POST']) #Define una ruta en la aplicación para manejar solicitudes POST a /assign_support.
def assign_support():
    data = request.get_json() #request.get_json(): Obtiene los datos JSON de la solicitud.

    description = data.get('description') #Obtiene la descripcion y la complegidad.
    complejidad = data.get('complejidad')

    # Obtener al trabajador con la menor carga de complejidad acumulada
    trabajador = Trabajador.query.order_by(Trabajador.compleacomulada).first() # Utiliza SQLAlchemy para obtener al primer trabajador ordenado por la carga de complejidad acumulada de manera ascendente.

    # Asignar el soporte al trabajador
    support = Support(description=description, complejidad=complejidad, trabajador_id=trabajador.id) #Crea una instancia de la clase Support con la información proporcionada y el ID del trabajador asignado
    db.session.add(support) #Agrega el nuevo soporte a la sesión de la base de datos para su posterior commit.

    # Actualizar la carga de complejidad acumulada del trabajador
    trabajador.compleacomulada += complejidad # Incrementa la carga de complejidad acumulada del trabajador con la complejidad del nuevo soporte.
    db.session.commit() #Realiza el commit en la base de datos para guardar los cambios.

    return jsonify({"message": f"El Soporte se le asigno a {trabajador.name}"}), 201 #Devuelve una respuesta JSON.

@app.route('/trabajador', methods=['GET']) #Define una ruta en la aplicación para manejar solicitudes GET a /trabajador.
def get_trabajadores():
    trabajadores = Trabajador.query.all()
    trabajadores_data = [{"name": trabajador.name, "compleacomulada": trabajador.compleacomulada} for trabajador in trabajadores]
    return jsonify(trabajadores_data) #Obtiene todos los trabajadores de la base de datos y devuelve sus datos en formato JSON.

if __name__ == '__main__':
    app.run(debug=True) #Si el script se ejecuta directamente (no importado como un módulo), la aplicación se ejecutará en modo de depuración (debug=True).