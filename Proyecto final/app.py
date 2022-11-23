from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from encript import bcrypt
from flask_migrate import Migrate
from config import BaseConfig

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
