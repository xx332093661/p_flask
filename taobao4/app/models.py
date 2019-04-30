# -*- coding: utf-8 -*-

from . import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    key_word = db.Column(db.String(100))
    product_id = db.Column(db.String(50))
    product_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    spec = db.Column(db.String(255))
    package_num = db.Column(db.String(10))
    unit = db.Column(db.String(200))
    price = db.Column(db.String(10))
    unit_price = db.Column(db.String(10))
    sales = db.Column(db.Integer)
    url = db.Column(db.String(200))
    nick = db.Column(db.String(200))
    product_file_id = db.Column(db.Integer, db.ForeignKey('product_file.id'))
    origin = db.Column(db.String(50))


class ProductFile(db.Model):
    __tablename__ = 'product_file'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    create_date = db.Column(db.DateTime(50), default=datetime.now())
    products = db.relationship('Product', backref='product_file', lazy='dynamic')
    state = db.Column(db.String(20))




