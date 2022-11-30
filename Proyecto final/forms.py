from flask import Flask
from flask_wtf import FlaskForm 
from models import Producto
from wtforms import StringField,SubmitField  
from wtforms.validators import DataRequired

class ProductoForm(FlaskForm): 
    id_producto= StringField('Id_producto',validators=[DataRequired()])
    nombre= StringField('Nombre',validators=[DataRequired()])
    categoria = StringField('Categoria',validators=[DataRequired()]) 
    serie = StringField('Serie',validators=[DataRequired()]) 
    enviar = SubmitField('Enviar')     

class UserForm(FlaskForm): 
    email= StringField('Email',validators=[DataRequired()])
    password= StringField('Password',validators=[DataRequired()])
    enviar = SubmitField('Enviar')
