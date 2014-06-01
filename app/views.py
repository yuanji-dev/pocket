# -*- coding: utf-8 -*-
from flask import Blueprint, flash
from flask import render_template, redirect, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import User, Item, Tag
from forms import LoginForm, RegisterForm, AddItemForm
from app import db
#todo add use readability to parse url?

main = Blueprint('main', __name__)


@main.before_app_request  #todo what does this mean?
def before_request():
    if current_user.is_authenticated():
        if not current_user.is_confirmed:
            return "you are not confirmed."


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


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item(link=form.link.data)
        # todo add error handler.
        item.parse_html()
        if form.tags.data:
            tags = form.tags.data.split(',')
            for tag in tags:
                if Tag.query.filter_by(name=tag).first():
                    item.tags.append(Tag.query.filter_by(name=tag).first())
                else:
                    item.tags.append(Tag(name=tag))
        current_user.items.append(item)
        db.session.add(current_user)
        db.session.commit()
        flash('a new item added.')
        return redirect(url_for('.index'))
    return render_template('add.html', form=form)


@main.route('/del/<id>')
@login_required
def delete(id):
    item = Item.query.filter_by(id=id).first()
    current_user.items.remove(item)
    db.session.add(current_user)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/a/<id>')
@login_required
def a(id):
