# coding: utf-8
from taobao_test import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)

    nid = db.Column(db.String(100))
    category = db.Column(db.String(50))
    title = db.Column(db.String(200))
    view_price = db.Column(db.String(100))
    item_loc = db.Column(db.String(200))
    view_sales = db.Column(db.String(255))
    nick = db.Column(db.String(200))

    url = db.Column(db.String(200))
    product_file_id = db.Column(db.Integer, db.ForeignKey('product_file.id'))

    def __init__(self, nid=None, category=None, title=None, view_price=None, item_loc=None, view_sales=None, nick=None,
                 url=None, product_file_id=None):

        self.nid = nid
        self.category = category
        self.title = title
        self.view_price = view_price
        self.item_loc = item_loc
        self.view_sales = view_sales
        self.nick = nick
        self.url = url
        self.product_file_id = product_file_id
