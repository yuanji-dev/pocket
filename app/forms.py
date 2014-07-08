# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, URL
from wtforms import ValidationError
from models import User
# todo add i18n support.

class LoginForm(Form):
    # length?
    # add remember me option.
    email = StringField(u'电子邮件',
                        validators=[Required(message=u'此项必须填写！'), Length(1, 64), Email(message=u'请输入正确的电子邮件！')])
    password = PasswordField(u'密码', validators=[Required(message=u'此项必须填写！')])
    remember = BooleanField(u'记住账号')
    submit = SubmitField(u'登录')


class RegisterForm(Form):
    email = StringField(u'电子邮件',
                        validators=[Required(message=u'此项必须填写！'), Length(1, 64), Email(message=u'请输入正确的电子邮件！')])
    # todo add re check.
    username = StringField(u'用户名', validators=[Required(message=u'此项必须填写！')])
    password = PasswordField(u'密码',
                             validators=[Required(message=u'此项必须填写！'), EqualTo('repassword', message=u'密码不匹配！')])
    repassword = PasswordField(u'重复密码', validators=[Required(message=u'此项必须填写！')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'此邮箱「{}」已被注册！'.format(field.data))

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(u'用户名「{}」已被注册！'.format(field.data))


# todo add validators and length limit.
class AddItemForm(Form):
    link = StringField(u'链接', validators=[Required(message=u'此项必须填写！'), URL(message=u"请输入有效的URL！")])
    tags = StringField(u'标签')
    submit = SubmitField(u'添加')


class SearchForm(Form):
    keyword = StringField('Keyword', validators=[Required()])


class EditItemForm(Form):
    title = StringField(u'标题', validators=[Required(message=u'此项必须填写！')])
    # link = StringField(u'链接', validators=[Required(message=u'此项必须填写！'), URL(message=u"请输入有效的URL！")])
    tags = StringField(u'标签')
    submit = SubmitField(u'更新')


class ChangePasswordForm(Form):
    current_password = PasswordField(u'旧密码', validators=[Required(message=u'此项必须填写！')])
    new_password = PasswordField(u'新密码',
                                 validators=[Required(message=u'此项必须填写！'),
                                             EqualTo('repassword', message=u'密码不匹配！')])
    repassword = PasswordField(u'重复新密码', validators=[Required(message=u'此项必须填写！')])
    submit = SubmitField(u'更新')


class DropAllForm(Form):
    password = PasswordField(u'密码', validators=[Required(message=u'此项必须填写！')])
    submit = SubmitField(u'清除')
