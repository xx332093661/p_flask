# -*-coding: utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .. import documents


class UploadForm(FlaskForm):
    document = FileField(u'上传文件', validators=[
        FileAllowed(documents, u'请上传excel文件！'),
        FileRequired(u'文件未选择！')])
    origin = SelectField(u'爬取网站', choices=[('taobao', u'淘宝'), ('vip', u'唯品会'), ('jd', u'京东')])
    submit = SubmitField(u'上传')
