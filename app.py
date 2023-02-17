from flask import Flask, jsonify, request
from flask_login import LoginManager
from models import Usuario,db
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app


app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})
#Configuracion login
app.secret_key = 'secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Configurar la extensión Flask-JWT-Extended
jwt = JWTManager(app)


@app.route('/registro', methods=['POST'])
def register():
    usuario = request.json.get('usuario', None)
    contraseña = request.json.get('contraseña', None)
    tipo = request.json.get('tipo', None)

    if not usuario or not contraseña:
        return jsonify({"msg": "Son necesarios el usuario y la contraseña."}), 400

    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({"msg": "Este usuario ya existe."}), 400
    

    user = Usuario(usuario=usuario, contraseña=generate_password_hash(contraseña), tipo=tipo)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully."}), 201

@app.route('/login', methods=['POST'])
def login():
    usuario = request.json.get('usuario', None)
    contraseña = request.json.get('contraseña', None)

    if not usuario or not contraseña:
        return jsonify({"msg": "Son necesarios el usuario y la contraseña."}), 400

    usuario = Usuario.query.filter_by(usuario=usuario).first()

    if not usuario or not check_password_hash(usuario.contraseña, contraseña):
        return jsonify({"msg": "contraseña o usuario invalido."}), 401

    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
