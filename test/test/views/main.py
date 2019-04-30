# coding: utf-8
from test import app
from flask import render_template, request, jsonify
from test.models.forms import LoginForm

import re


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', form=form)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    return render_template('calculator.html')


@app.route('/_calculate')
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