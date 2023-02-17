from flask import jsonify, request
from flask_restful import Resource, reqparse
from models import Parada,Hora,Bus,Ruta,Usuario,db
from app import app
from datetime import datetime
from flask_jwt_extended import jwt_required
# Definir una vista de RESTful para el modelo Parada

class ParadaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', type=str, required=True, help='Nombre de la parada es requerido')
    parser.add_argument('latitud', type=float, required=True, help='Latitud de la parada es requerido')
    parser.add_argument('longitud', type=float, required=True, help='Longitud de la parada es requerido')

    @jwt_required()
    def get(self, id):
        parada = Parada.query.filter_by(id=id).first()
        if parada:
            return jsonify({'id': parada.id, 'nombre': parada.nombre, 'latitud': parada.latitud, 'longitud': parada.longitud})
        else:
            return {'message': 'Parada no encontrada'}, 404

    @jwt_required()
    def post(self):
        data = ParadaResource.parser.parse_args()
        parada = Parada(nombre=data['nombre'], latitud=data['latitud'], longitud=data['longitud'])
        db.session.add(parada)
        db.session.commit()
        return {'message': 'Parada creada', 'id': parada.id}, 201


# Definir una vista de RESTful para el modelo Bus
class BusResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('placa', type=str, required=True, help='Placa del bus es requerida')

    @jwt_required()
    def get(self, id):
        bus = Bus.query.filter_by(id=id).first()
        if bus:
            return jsonify({'id': bus.id, 'placa': bus.placa})
        else:
            return {'message': 'Bus no encontrado'}, 404

    @jwt_required()
    def post(self):
        data = BusResource.parser.parse_args()
        bus = Bus(placa=data['placa'])
        db.session.add(bus)
        db.session.commit()
        return {'message': 'Bus creado', 'id': bus.id}, 201


# Definir una vista de RESTful para el modelo Hora
class HoraResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('hora', type=str, required=True, help='Hora es requerida')

    @jwt_required()
    def get(self, id):
        hora = Hora.query.filter_by(id=id).first()
        if hora:
            return jsonify({'id': hora.id, 'hora': str(hora.hora)})
        else:
            return {'message': 'Hora no encontrada'}, 404

    @jwt_required()
    def post(self):
        data = HoraResource.parser.parse_args()
        hora = Hora(hora=data['hora'])
        db.session.add(hora)
        db.session.commit()
        return {'message': 'Hora creada', 'id': hora.id}, 201


# Definir una vista de RESTful para el modelo Ruta
class RutaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', type=str, required=True, help='Nombre de la ruta es requerido')
    parser.add_argument('parada_id', type=int, required=True, help='ID de la parada es requerido')
    parser.add_argument('bus_id', type=int, required=True, help='ID del bus es requerido')
    parser.add_argument('hora_id', type=int, required=True, help='ID de la hora es requerido')

    @jwt_required()
    def get(self, id):
        ruta = Ruta.query.filter_by(id=id).first()
        if ruta:
            return jsonify({'id': ruta.id, 'nombre': ruta.nombre, 'parada_id': ruta.parada_id, 'bus_id': ruta.bus_id, 'hora_id': ruta.hora_id})
        else:
            return {'message': 'Ruta no encontrada'}, 404

    @jwt_required()
    def post(self):
        data = RutaResource.parser.parse_args()
        ruta = Ruta(nombre=data['nombre'], parada_id=data['parada_id'], bus_id=data['bus_id'], hora_id=data['hora_id'])
        db.session.add(ruta)
        db.session.commit()
        return {'message': 'Ruta creada', 'id': ruta.id}, 201


# Definir una vista de RESTful para el modelo Usuario
class UsuarioResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('usuario', type=str, required=True, help='nombre de usuario es requerido')
    parser.add_argument('contraseña', type=int, required=True, help='Contraseña del usuario es requerido')
    parser.add_argument('tipo', type=int, required=True, help='TIPO de usuario es requerido')

    @jwt_required()
    def get(self, id):
        usuario = Usuario.query.filter_by(id=id).first()
        if usuario:
            return jsonify({'id': usuario.id, 'usuario': usuario.usuario, 'contraseña': usuario.contraseña, 'tipo': usuario.tipo})
        else:
            return {'message': 'Usuario no encontrado'}, 404

    @jwt_required()
    def post(self):
        data = RutaResource.parser.parse_args()
        usuario = Ruta(usuario=data['usuario'], contraseña=data['contraseña'], tipo=data['tipo'])
        db.session.add(usuario)
        db.session.commit()
        return {'message': 'Usuario creado', 'id': usuario.id}, 201
    

# Funcion para valores de parada
@app.route('/horasiguiente', methods=['POST'])
@jwt_required()
def Horasiguiente():
    id = request.json.get('id', None)
    hora = request.json.get('hora', None)
    rutas = Ruta.query.all()
    parada = Parada.query.filter_by(id=id).first()
    rutafin = None
    hora_minima=None
    horita=None
    hora = datetime.strptime(hora, '%H:%M:%S').time()
    if parada:
        for ruta in rutas:
            actualhora = Hora.query.filter_by(id=ruta.hora_id).first()
            if ruta.parada_id == parada.id and actualhora.hora >= hora:
                if hora_minima is None or hora_minima >= actualhora.hora:
                    hora_minima=actualhora.hora
                    rutafin=ruta

            if ruta.parada_id == parada.id and actualhora.hora <= hora:
                if horita is None or horita >= actualhora.hora:
                    horita=actualhora.hora
                    ultimaruta=ruta
        
        if rutafin is None:
            rutafin = ultimaruta

        busF=Bus.query.filter_by(id=rutafin.bus_id).first()
        horaF=Hora.query.filter_by(id=rutafin.hora_id).first()


        return jsonify({'parada': parada.nombre, 'bus': busF.placa, 'hora': str(horaF.hora), 'longitud': parada.longitud, 'latitud': parada.latitud})
    else:
        return {'message': 'Parada no encontrada'}, 404

@app.route('/rutaproxima', methods=['POST'])
@jwt_required()
def Rutaproxima():
    hora = request.json.get('hora', None)
    hora = datetime.strptime(hora, '%H:%M:%S').time()
    rutas = Ruta.query.all()
    hora_minima=None
    rutafin = None
    for ruta in rutas:
        actualhora = Hora.query.filter_by(id=ruta.hora_id).first()
        if actualhora.hora >= hora:
            if hora_minima is None or hora_minima >= actualhora.hora:
                hora_minima=actualhora.hora
                rutafin=ruta
    rutas_finales = Ruta.query.filter_by(hora_id=rutafin.hora_id).all()
    rutas_json = [{'paradas':Parada.query.filter_by(id=ruta_final.parada_id).first().nombre,
                   'bus':Bus.query.filter_by(id=ruta_final.bus_id).first().placa,
                   'hora':str(Hora.query.filter_by(id=rutafin.hora_id).first().hora),
                   'longitud':Parada.query.filter_by(id=ruta_final.parada_id).first().longitud,
                   'latitud':Parada.query.filter_by(id=ruta_final.parada_id).first().latitud
                   } for ruta_final in rutas_finales]
    return jsonify(rutas_json)

