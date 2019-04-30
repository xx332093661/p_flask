# coding: utf-8
from taobao3 import db


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

    def __init__(self, key_word=None, product_id=None, product_name=None, address=None, spec=None, package_num=None, unit=None,
                 price=None, unit_price=None, sales=None, url=None, nick=None, product_file_id=None, origin=None):
        self.key_word = key_word
        self.product_id = product_id
        self.product_name = product_name
        self.address = address
        self.spec = spec
        self.package_num = package_num
        self.unit = unit
        self.price = price
        self.unit_price = unit_price
        self.sales = sales
        self.url = url
        self.nick = nick
        self.product_file_id = product_file_id
        self.origin = origin
