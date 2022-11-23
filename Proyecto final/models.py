import jwt
import datetime
from config import BaseConfig
from app import db,bcrypt

class User(db.Model):
    __tablename__ ="users"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255),nullable=False)
    registered_on = db.Column(db.DateTime,nullable=False)
    admin = db.Column(db.Boolean,nullable=False,default=False)

    def __init__(self,email,password,admin=False) -> None:
        self.email=email
        self.password=bcrypt.generate_password_hash(password,BaseConfig.BCRYPT_LOG_ROUNDS).decode()
        self.registered_on=datetime.datetime.now()
        self.admin=admin

    def encode_auth_token(self,user_id):
        try:
            payload={
                'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1,minutes=10),
                'iat':datetime.datetime.utcnow(),
                'sub':user_id
            }
            return jwt.encode(payload,BaseConfig.SECRET_KEY,algorithm="HS256")
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        try :
            payload = jwt.decode(auth_token,BaseConfig.SECRET_KEY,algorithms=['HS256'])
            return payload('sub')
        except jwt.ExpiredSignatureError as e:
            return "Token expirado"
        except jwt.InvalidTokenError as e:
            return "Token no valido"

class Images(db.Model):
    __tablename__ = 'user_images' 

    id_imagen = db.Column(db.Integer,  primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
    rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # define relationship
    region = db.relationship('User', backref='users')

    def __repr__(self):
        return f'Pic ID: {self.id} Data: {self.data} text: {self.text} user: {self.user_id}'

class Producto (db.Model):
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    categoria = db.Column(db.String(250))
    serie = db.Column(db.String(250))
    
    def __str__(self) -> str:
        return (f'ID producto:{self.id_producto},'
                f'Nombre:{self.nombre},' 
                f'Categoria:{self.categoria},'
                f'Serie:{self.serie}')