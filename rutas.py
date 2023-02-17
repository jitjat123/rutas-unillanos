from models import Parada,Bus,Hora,Ruta,Usuario
from app import app,db
from views import ParadaResource,BusResource,HoraResource,RutaResource,UsuarioResource
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_restful import Api

admin = Admin(app, name='Panel administrativo', template_mode='bootstrap3')
admin.add_view(ModelView(Parada, db.session))
admin.add_view(ModelView(Bus, db.session))
admin.add_view(ModelView(Hora, db.session))
admin.add_view(ModelView(Ruta, db.session))
admin.add_view(ModelView(Usuario, db.session))


api = Api(app)
api.add_resource(ParadaResource, '/paradas', '/paradas/<int:id>')
api.add_resource(BusResource, '/buses', '/buses/<int:id>')
api.add_resource(HoraResource, '/horas', '/horas/<int:id>')
api.add_resource(RutaResource, '/rutas', '/rutas/<int:id>')
api.add_resource(UsuarioResource, '/usuarios', '/usuarios/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)