from flask import Blueprint,request,jsonify
from sqlalchemy import exc
from models import User
from app import db, bcrypt
from auth import tokenCheck
appUser = Blueprint('appUser',__name__,template_folder="template") #Aqui es donde ponemos el nombre de nuestras vistas, template puede ser cualquier nombre.

@appUser.route('/auth/registro',methods=['POST'])
def registro():
    user = request.get_json()
    userExist = User.query.filter_by(email=user['email']).first()
    if not userExist:
        usuario = User(email=user['email'],password=user["password"])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario Creado"
        except exc.SQLAlchemyError as e:
            mensaje="error"
    else:
        mensaje="El usuario ya existe"
    return jsonify({"mensaje":mensaje})


@appUser.route('/auth/login',methods={'POST'})
def login():
    user = request.get_json( )
    usuario = User(email=user['email'],password=user['password'])
    searchUser = User.query.filter_by(email=usuario.email).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,user["password"])
        if validation:
            auth_token= usuario.encode_auth_token(user_id=searchUser.id)
            responseObje = {
                "status":"exitoso",
                "mensaje":"Login",
                "auth_token":auth_token
            }
            return jsonify(responseObje)
    return jsonify({"mensaje":"Datos Incorrectos"})

@appUser.route('/usuarios', methods=['GET'])
@tokenCheck
def getUsers(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin']:
        output = []
        usuarios = User.query.all()
        for usuario in usuarios:
            usuarioData = {}
            usuarioData['id'] = usuario.id
            usuarioData['email'] = usuario.email
            usuarioData['password'] = usuario.password
            usuarioData['registered_on'] = usuario.registered_on
            usuarioData['admin'] = usuario.admin
            output.append(usuarioData)
        return jsonify({'usuarios':output})