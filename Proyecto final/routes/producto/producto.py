from flask import Blueprint,request,jsonify
from sqlalchemy import exc
from models import Producto,User
from app import db, bcrypt
from auth import tokenCheck
appProducto = Blueprint('appProducto',__name__,template_folder="template") #Aqui es donde ponemos el nombre de nuestras vistas, template puede ser cualquier nombre.

@appProducto.route('/producto',methods=['GET'])
@tokenCheck
def mostrarTodos(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin'] or not usuario['admin']:
        output = []
        productos = Producto.query.all()
        for producto in productos:
            productoData = {}
            productoData['id_producto'] = producto.id_producto
            productoData['nombre'] = producto.nombre
            productoData['categoria'] = producto.categoria
            productoData['serie'] = producto.serie
            output.append(productoData)
        return jsonify({'productos':output})

@appProducto.route('/producto/<int:id>',methods=['GET'])
@tokenCheck
def mostrarUno(id,usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin'] or not usuario['admin']:
        searchProducto = Producto.query.filter_by(id_producto=id).first()
        if searchProducto:
            responseObje = {
                "id_producto":searchProducto.id_producto,
                "nombre":searchProducto.nombre,
                "categoria":searchProducto.categoria,
                "serie" : searchProducto.serie
            }
            return jsonify(responseObje)
        return jsonify({"mensaje":"No existe el producto!"})


@appProducto.route('/producto',methods={'POST'})
@tokenCheck
def registro(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin'] or not usuario['admin']:
        product = request.get_json( )
        productoExists = Producto.query.filter_by(id_producto=product['id_producto']).first()
        if  not productoExists:
            producto = Producto(id_producto=product['id_producto'],nombre=product['nombre'],categoria=product['categoria'],serie=product['serie'])
            try:
                db.session.add(producto)
                db.session.commit()
                mensaje="Producto creado!"
            except exc.SQLAlchemyError as e:
                mensaje = "error: " + e
        else:
            mensaje = "El producto ya existe"
        return jsonify({"mensaje":mensaje})

@appProducto.route('/producto', methods=['PATCH'])
@tokenCheck
def actualizar(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin'] or not usuario['admin']:
        product = request.get_json( )
        searchProducto = Producto.query.filter_by(id_producto=product['id_producto']).first()
        if  searchProducto:
            try:
                searchProducto.nombre = product['nombre']
                searchProducto.categoria = product['categoria']
                searchProducto.serie = product['serie']
                db.session.commit()
                mensaje="Producto actualizado!"
            except exc.SQLAlchemyError as e:
                mensaje = "error: " + e
        else:
            mensaje = "El producto no existe!"
        return jsonify({"mensaje":mensaje})


@appProducto.route('/producto/<int:id>', methods=['DELETE'])
@tokenCheck
def borrarUno(usuario,id):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin']:
        searchProducto = Producto.query.filter_by(id_producto=id).first()
        if searchProducto:
            db.session.delete(searchProducto)
            db.session.commit()
            return jsonify({"mensaje":"Producto eliminado!"})
        return jsonify({"mensaje":"No existe el producto!"})
    return jsonify({"mensaje":"Esta acción solamente es permitida por administradores!"})

@appProducto.route('/producto', methods=['DELETE'])
@tokenCheck
def borrarTodos(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin']:
        db.session.query(Producto).delete()
        db.session.commit()
        return "Productos eliminados!"
    return jsonify({"mensaje":"Esta acción solamente es permitida por administradores!"})
