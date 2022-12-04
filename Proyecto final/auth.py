from models import User
from functools import wraps
from flask import render_template, request

def obtenerInfo(token):
    if token:
        resp = User.decode_auth_token(token)
        user = User.query.filter_by(id=resp).first()
        if  user:
            usuario = {
                    'status': 'success',
                    'admin': user.admin
                }
            return usuario
        else:
            error = {
                'status': 'fail',
                'message': resp
            }
            return error


def tokenCheck(f):
    @wraps(f)
    def verificar(*args, **kwargs):
        token = None

        token = request.form['token']
    
        try:
            info = obtenerInfo(token)
            if info['status'] == "fail":
                return render_template('error.html', 
                error = 'El token es inválido')
        except:
            return render_template('error.html', 
            error = 'El token es inválido')
        return (info['admin'])
    return verificar

