# coding: utf-8
from taobao_test import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class
from flask_bootstrap import Bootstrap
from wtforms import SubmitField, SelectField
from flask import render_template, Flask, request
from taobao_test.models.files import ProductFile
from taobao_test import db
from flask import make_response
from tmgj import tmgj_spider
from tmcs import tmcs_spider
from tools import get_data


import traceback
import tablib
import threading

documents = UploadSet('documents', DOCUMENTS)
configure_uploads(app, documents)
patch_request_class(app)  # 文件大小限制，默认为16MB
bootstrap = Bootstrap(app)





class UploadForm(FlaskForm):
    document = FileField(u'上传文件', validators=[
        FileAllowed(documents, u'请上传excel文件！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')


class SelectForm(FlaskForm):
    origin = SelectField(u'数据', choices=[
        ('tmgj', u'天猫国际'),
        ('tmcs', u'天猫超市'),
    ])
    submit = SubmitField(u'确定')


@app.route('/', methods=['GET', 'POST'])
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    form = SelectForm()

    datas = []
    if form.validate_on_submit():
        try:
            if form.origin.data == 'tmgj':
                # 开启线程
                t = threading.Thread(target=tmgj_spider)
            else:
                t = threading.Thread(target=tmcs_spider)
            t.setDaemon(True)
            t.start()

            return render_template('index.html', show_msg=1)
        except Exception:
            return traceback.format_exc()

    return render_template('index.html', form=form, datas=datas)


@app.route('/get_file_list', methods=['GET', 'POST'])
def get_file_list():

    product_files = ProductFile.query.order_by(db.desc('id')).all()
    datas = []
    for product_file in product_files:
        datas.append({
            'id': product_file.id,
            'name': product_file.name,
            'create_date': product_file.create_date,
            'state': product_file.state
        })

    return render_template('files.html', datas=datas)


@app.route('/get_datas/<int:product_file_id>')
def get_datas(product_file_id=None):
    datas = get_data(product_file_id)
    return render_template('data.html', datas=datas)


@app.route('/export_excel', methods=['POST'])
def export_excel():
    if request.method == 'POST':
        headers = (u"nid", u"category", u"title", u"view_price", u'item_loc', u'view_sales', u'nick')

        product_file_id = request.form['kwds']

        datas = get_data(product_file_id)

        rows = [
        ]
        for data in datas:
            rows.append(
                (data['nid'], data['category'], data['title'], data['view_price'], data['item_loc'], data['view_sales'], data['nick'])
            )

        data = tablib.Dataset(*rows, headers=headers)

        resp = make_response(data.xlsx)

        resp.headers["Content-Disposition"] = "attachment; filename=产品.xlsx"

        return resp


