# -*- coding: utf-8 -*-
from flask import Blueprint, flash
from flask import render_template, redirect, url_for
from flask.ext.login import login_user, login_required, logout_user
from models import User
from forms import LoginForm, RegisterForm
from app import db
#todo add use readability to parse url?

main = Blueprint('main', __name__)


@main.route('/')
#@login_required  #login message?
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            #todo remember time fresh? how long remember?
            login_user(user, form.remember.data)
            return redirect(url_for('.index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('you have successfully registered an account.')
        return redirect(url_for('.index'))
    return render_template('register.html', form=form)