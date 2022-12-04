from flask import Flask,render_template,request,session,url_for,jsonify
from flask_cors import CORS
from database import db
from encript import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from auth import tokenCheck


from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from models import User

from routes.user.user import appUser
from routes.images.images import imageUser
from routes.producto.producto import appProducto

import logging
app = Flask(__name__)

app.register_blueprint(appUser)
app.register_blueprint(imageUser)
app.register_blueprint(appProducto)
app.config.from_object(BaseConfig)

CORS(app)
bcrypt.init_app(app)
db.init_app(app)

migrate = Migrate(app)
migrate.init_app(app,db)


logging.basicConfig(filename="error.log",level=logging.DEBUG)

@app.route('/')
@app.route('/menu')
def inicio(): 
    if 'user' in session:
        usuario =  session['user']
        searchUser = User.query.filter_by(email = usuario).first()
        token = searchUser.encode_auth_token(user_id=searchUser.id)
        return render_template('menuPrincipal.html',token = token, user = searchUser.email)
    else:
        return redirect(url_for('appUser.login'))


@app.route('/salir')
def salir():
    session.pop('user')
    return render_template('error.html', error='Favor de iniciar sesion nuevamente')


