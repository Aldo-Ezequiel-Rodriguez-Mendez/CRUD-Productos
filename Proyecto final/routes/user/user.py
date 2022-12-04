from flask import Blueprint,render_template,url_for,request,session,jsonify
from sqlalchemy import exc
from models import User
from app import db, bcrypt
from auth import obtenerInfo, tokenCheck
from werkzeug.utils import redirect
from werkzeug.exceptions import abort

appUser = Blueprint('appUser',__name__,template_folder="template") #Aqui es donde ponemos el nombre de nuestras vistas, template puede ser cualquier nombre.


@appUser.route('/agregarUsuario',methods=['GET','POST'])
def registroUsuario():
    usuario = User(email="",password="")
    usuarioForm = User(obj=usuario)
    if request.method == "POST":
        if usuarioForm.validate_on_submit():
            usuarioForm.populate_obj(usuario)
            searchUsuario = User.query.filter_by(email=usuario.email).first()
            if not searchUsuario:
                #insert
                db.session.add(usuario)
                db.session.commit()
                return redirect(url_for('inicio'))
            return render_template('error.html', error ='El usuario ya existe!')
    return render_template('agregarUsuario.html',forma = usuarioForm)


@appUser.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        searchUser = User.query.filter_by(email=request.form['email']).first()
        session['user'] = ''
        if searchUser:
            validation = bcrypt.check_password_hash(searchUser.password,request.form['password'])
            if validation:
                session['user'] = searchUser.email
                return redirect(url_for('inicio',usuario = searchUser.email))
            return redirect (url_for('salir'))
        return redirect (url_for('salir'))
    return render_template('login.html')

@appUser.route('/usuarios/<string:token>')
def verUsuarios(token):
    admin = obtenerInfo(token)
    if admin['admin']:
        usuarios = User.query.all()
        return render_template('indexUsuario.html', usuarios = usuarios,token = token)
    return render_template('error.html', error='Solamente se permite acceso a los administradores :(')