from flask import Blueprint, redirect, render_template,request,jsonify, url_for
from sqlalchemy import exc
from forms import ProductoForm
from models import Producto,User
from app import db, bcrypt
from auth import obtenerInfo, tokenCheck
appProducto = Blueprint('appProducto',__name__,template_folder="template") #Aqui es donde ponemos el nombre de nuestras vistas, template puede ser cualquier nombre.

@appProducto.route('/productos/<string:token>',methods=['GET'])
def verProductos(token):
    admin = obtenerInfo(token)
    if admin['admin'] or not admin['admin']:
        productos = Producto.query.all()
        return render_template('indexProducto.html', productos = productos,token = token) 

@appProducto.route('/producto/<int:id>/<string:token>',methods=['GET'])
def mostrarUno(id,token):
    admin = obtenerInfo(token)
    if admin['admin'] or not admin['admin']:
        searchProducto = Producto.query.filter_by(id_producto=id).first()
        if searchProducto:
            return render_template('detalleProducto.html', producto=searchProducto)
        return render_template('error.html', error ='No existe el producto!')


@appProducto.route('/agregarProducto/<string:token>',methods=['GET','POST'])
def registroProducto(token):
    admin = obtenerInfo(token)
    if admin['admin'] or not admin['admin']:
        producto = Producto(id_producto='',nombre='',categoria='',serie='')
        productoForm = ProductoForm(obj=producto)
        if request.method == "POST":
            if productoForm.validate_on_submit():
                productoForm.populate_obj(producto)
                searchProducto = Producto.query.filter_by(id_producto=producto.id_producto).first()
                if not searchProducto:
                    #insert
                    db.session.add(producto)
                    db.session.commit()
                    return redirect(url_for('inicio'))
                return render_template('error.html', error ='El producto ya existe!')
        return render_template('agregarProducto.html',forma = productoForm)

@appProducto.route('/editar/<int:id>/<string:token>', methods=['GET','POST'])
def actualizar(id,token):
    admin = obtenerInfo(token)
    if admin['admin'] or not admin['admin']:
        searchProducto = Producto.query.filter_by(id_producto=id).first()
        if searchProducto:
            productoForm = ProductoForm(obj=searchProducto)
            if request.method == "POST":
                if productoForm.validate_on_submit():
                    productoForm.populate_obj(searchProducto)
                    db.session.commit()
                    return  redirect(url_for('inicio'))
            return render_template('editarProducto.html',forma = productoForm)
        return render_template('error.html', error ='No existe el producto!')
    


@appProducto.route('/eliminar/<int:id>/<string:token>')
def borrarUno(id,token):
    admin = obtenerInfo(token)
    if admin['admin']:
        searchProducto = Producto.query.filter_by(id_producto=id).first()
        if searchProducto:
            db.session.delete(searchProducto)
            db.session.commit()
            return redirect(url_for('inicio'))
        return render_template('error.html', error ='No existe el producto!')
    return render_template('error.html', error='Esta acción solamente es permitida por administradores!')

@appProducto.route('/eliminarTodo/<string:token>')
def borrarTodos(token):
    admin = obtenerInfo(token)
    if admin['admin']:
        db.session.query(Producto).delete()
        db.session.commit()
        return redirect(url_for('inicio'))
    return render_template('error.html', error='Esta acción solamente es permitida por administradores!')
