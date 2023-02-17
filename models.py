
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cadena12@localhost/rutas'


class Parada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)

    def __repr__(self):
        return f'<{self.nombre}>'

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10))

    def __repr__(self):
        return f'<{self.placa}>'

class Hora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hora = db.Column(db.Time)

    def __repr__(self):
        return f'<{self.hora}>'
    

class Ruta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parada_id = db.Column(db.Integer, db.ForeignKey('parada.id'))
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    hora_id = db.Column(db.Integer, db.ForeignKey('hora.id'))
    nombre = db.Column(db.String(100))

    parada = db.relationship('Parada', backref=db.backref('rutas', lazy=True))
    bus = db.relationship('Bus', backref=db.backref('rutas', lazy=True))
    hora = db.relationship('Hora', backref=db.backref('rutas', lazy=True))

    def __repr__(self):
        return f'<Ruta {self.nombre}>'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


