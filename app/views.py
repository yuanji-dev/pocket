# -*- coding: utf-8 -*-
from flask import Blueprint, flash
from flask import render_template, redirect
from flask.ext.login import login_user, login_required, logout_user
from models import User
from forms import LoginForm

main = Blueprint('index', __name__)


@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        flash('Invalid email or password')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect('/')


@main.route('/register')
def register():
    #todo add register view