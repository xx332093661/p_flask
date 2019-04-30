# coding: utf-8

from manage import app
from flask import render_template, request, jsonify
from . import main
from flask_login import login_required, current_user

import re


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        photos = current_user.followed_photos
        photos = [photo for photo in photos if photo.album.no_public == False]
    else:
        photos = ""
    return render_template('index.html', photos=photos)


@main.route('/calculator', methods=['GET', 'POST'])
def calculator():
    return render_template('calculator.html')


@main.route('/_calculate')
def calculate():
    a = request.args.get('number1', '0')
    operator = request.args.get('operator', '+')
    b = request.args.get('number2', '0')
    m = re.match('-?\d+', a)
    n = re.match('-?\d+', b)
    if m is None or n is None or operator not in '+-*/':
        return jsonify(result='I Catch a BUG!')
    if operator == '/':
        result = eval(a + operator + str(float(b)))
    else:
        result = eval(a + operator + b)
    return jsonify(result=result)

