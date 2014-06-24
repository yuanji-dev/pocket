# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request, g
from flask import render_template, redirect, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import User, Item, Tag
from forms import LoginForm, RegisterForm, AddItemForm, SearchForm
from app import db
from parse_html import parse_html

#todo add modify item func. eg:title etc.
#todo add search func. use ajax to auto-complete.
#todo add participle as tag?
#todo add pagination
# todo add rss subscription.
main = Blueprint('main', __name__)


@main.before_app_request  #todo what does this mean?
def before_request():
    g.search_form = SearchForm()
    if current_user.is_authenticated():
        if not current_user.is_confirmed:
            return "you are not confirmed."


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            #todo remember time fresh? how long remember?
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('.index'))
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
        # item.parse_html()
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
        parse_html(item.id)
        flash('a new item added.')
        return redirect(url_for('.index'))
    return render_template('add.html', form=form)


@main.route('/del/<id>')
@login_required
def delete(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if not item or item not in items:
        flash('no such item.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        current_user.items.remove(item)
        db.session.add(current_user)
        db.session.delete(item)
        db.session.commit()
        flash('delete successfully.')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/a/<id>')
@login_required
def a(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if item not in items:
        flash('this item is not yours.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('a.html', item=item, title=item.title)


@main.route('/star/<id>')
@login_required
def star(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if item not in items:
        flash('this item is not yours.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_star = True
        db.session.add(item)
        db.session.commit()
        flash('you starred the item.')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/unstar/<id>')
@login_required
def unstar(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if item not in items:
        flash('this item is not yours.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_star = False
        db.session.add(item)
        db.session.commit()
        flash('you destarred the item.')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/tag/<name>')
@login_required
def tag(name):
    all_items = current_user.items.all()
    items = []
    for item in all_items:
        if name in item.get_tags():
            items.append(item)
    if not items:
        flash('not item has this tag.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('tag.html', items=items, tag=name)


@main.route('/stars')
@login_required
def stars():
    items = current_user.items.filter_by(is_star=True).all()
    if not items:
        flash('not star item.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('stars.html', items=items)


# todo add complete the search func.
@main.route('/query', methods=['POST'])
@login_required
def query():
    if g.search_form.validate_on_submit():
        return redirect(url_for('.search', keyword=g.search_form.keyword.data))
    return redirect(url_for('.index'))


# todo:fix a bug, if keyword is '/'
@main.route('/search/<keyword>', methods=['GET', 'POST'])
@login_required
def search(keyword):
    items = Item.query.filter(Item.user == current_user, Item.title.like('%' + keyword + '%')).all()
    if not items:
        flash('no such items.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('search.html', items=items, keyword=keyword)


@main.route('/archives')
@login_required
def archives():
    items = Item.query.filter(Item.user == current_user, Item.is_archive == True).all()
    if not items:
        flash('no such items.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('archives.html', items=items)


@main.route('/archive/<id>')
@login_required
def archive(id):
    item = Item.query.filter(Item.user == current_user, Item.id == id).first()
    if not item:
        flash('no such item.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_archive = True
        db.session.add(item)
        db.session.commit()
        flash('you archived the item.')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/unarchive/<id>')
@login_required
def unarchive(id):
    item = Item.query.filter(Item.user == current_user, Item.id == id).first()
    if not item:
        flash('no such item.')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_archive = False
        db.session.add(item)
        db.session.commit()
        flash('you unarchived the item.')
        return redirect(request.args.get('next') or url_for('.index'))