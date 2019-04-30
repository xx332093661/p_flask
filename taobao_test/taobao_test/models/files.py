# coding: utf-8
from taobao_test import db
from datetime import datetime


class ProductFile(db.Model):
    __tablename__ = 'product_file'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    create_date = db.Column(db.DateTime(50), default=datetime.now())
    products = db.relationship('Product', backref='product_file', lazy='dynamic')
    state = db.Column(db.String(20))

    def __init__(self, name=None, create_date=None, state=None):
        self.name = name
        self.state = state
        if create_date:
            self.create_date = create_date

