# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class JoinForm(Form):
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.'), validators.Email(u'이메일 형식이 아닙니다.')],
        description={'placeholder': u'Enter your e-mail'}
    )
    password = PasswordField(
        u'패스워드',
        [validators.data_required(u'패스워드를 입력하시기 바랍니다.'),
        validators.EqualTo('confirm_password', message=u'패스워드가 일치하지 않습니다.')],
        description={'placeholder': u'enter your password.'}
    )
    confirm_password = PasswordField(
        u'패스워드 확인',
        [validators.data_required(u'패스워드를 한번 더 입력하세요.')],
        description={'placeholder': u'confirm your password.'}
    )
    


class MajorForm(Form):
    major=StringField(
        u'학과명',
        [validators.data_required(u'학과명을 쓰세요.'),
        validators.length(max=15)],
        description={'placeholder':u'enter your major'}  
        )
    comments=StringField(
        u'한줄 평가',
        [validators.data_required(u'한 줄 평가하기!'),
        validators.length(max=45)],
        description={'placeholder': u'write a comment with length 45'}
    )
    extra_major=StringField(
        u'복전유무',
        [validators.data_required(u'복전유무')],
        description={'placeholder': u'confirm your extra major'}
    )
    