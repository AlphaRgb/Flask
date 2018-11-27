#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-11-05 17:18:26
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-11-05 17:18:40


from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField


class PostForm(FlaskForm):
    title = StringField('Title')
    body = CKEditorField('Body')
    submit = SubmitField('Submit')
