from models import User
from functools import wraps
from flask import request,jsonify

def obtenerInfo(token):
    if token:
        resp = User.decode_auth_token(token)
        user = User.query.filter_by(id=resp).first()
        if  user:
            usuario = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
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
        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'token no encontrado'})
        try:
            info = obtenerInfo(token)
            print(info)
            if info['status'] == "fail":
                return jsonify({'message': 'token is invalid'})
        except:
            return jsonify({'message': 'token is invalid'})
        print("hi")
        return f(info['data'], *args, **kwargs)
    return verificar