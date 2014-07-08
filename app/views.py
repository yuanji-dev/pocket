# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request, g
from flask import render_template, redirect, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import User, Item, Tag
from forms import LoginForm, RegisterForm, AddItemForm, SearchForm, EditItemForm, ChangePasswordForm, DropAllForm
from app import db
from parse_html import parse_html

# todo add tags page show all tags.
#todo add search func. use ajax to auto-complete.
#todo add participle as tag?
#todo add pagination
# todo add rss subscription.
main = Blueprint('main', __name__)


@main.before_app_request
def before_request():
    g.search_form = SearchForm()
    if current_user.is_authenticated():
        if not current_user.is_confirmed:
            return u"您的账号尚未被确认。"


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
            flash(u'「{} 」，您已成功登录！'.format(user.name), 'success')
            return redirect(request.args.get('next') or url_for('.index'))
        flash(u'账号或密码有误，请重新登录。', 'warning')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    flash(u'您的账号「{} 」以登出。'.format(current_user.name), 'info')
    logout_user()
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
        flash(u'恭喜：您成功注册了账号「{} 」。'.format(user.name), 'success')
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
        flash(u'已添加新条目：「{} 」。'.format(form.link.data), 'success')
        return redirect(url_for('.index'))
    return render_template('add.html', form=form)


@main.route('/del/<id>')
@login_required
def delete(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if not item or item not in items:
        flash('不存在该条目。', 'info')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item_title = item.title or item.link
        current_user.items.remove(item)
        db.session.add(current_user)
        db.session.delete(item)
        db.session.commit()
        flash(u'成功删除条目：「{} 」。'.format(item_title), 'success')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/a/<id>')
@login_required
def a(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if item not in items:
        flash(u'不存在该条目。', 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('a.html', item=item, title=item.title)


@main.route('/star/<id>')
@login_required
def star(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if item not in items:
        flash(u'不存在该条目。', 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_star = True
        item_title = item.title or item.link
        db.session.add(item)
        db.session.commit()
        flash(u'已为「{} 」添加星标。'.format(item_title), 'info')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/unstar/<id>')
@login_required
def unstar(id):
    item = Item.query.filter_by(id=id).first()
    items = current_user.items.all()
    if item not in items:
        flash(u'不存在该条目。', 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_star = False
        item_title = item.title or item.link
        db.session.add(item)
        db.session.commit()
        flash(u'已为「{} 」去除星标。'.format(item_title), 'info')
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
        flash(u'没有条目拥有标签：{}。'.format(name), 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('tag.html', items=items, tag=name)


@main.route('/stars')
@login_required
def stars():
    items = current_user.items.filter_by(is_star=True).all()
    if not items:
        flash(u'您目前没有任何星标条目。', 'warning')
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


# todo:fix a bug, if keyword is only '/'
@main.route('/search/<path:keyword>', methods=['GET', 'POST'])
@login_required
def search(keyword):
    items = Item.query.filter(Item.user == current_user, Item.title.like('%' + keyword + '%')).all()
    if not items:
        flash(u'没有搜到任何关于{}的条目，建议缩小关键词。'.format(keyword), 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('search.html', items=items, keyword=keyword)


@main.route('/archives')
@login_required
def archives():
    items = Item.query.filter(Item.user == current_user, Item.is_archive == True).all()
    if not items:
        flash(u'您目前没有任何存档条目。', 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        return render_template('archives.html', items=items)


@main.route('/archive/<id>')
@login_required
def archive(id):
    item = Item.query.filter(Item.user == current_user, Item.id == id).first()
    if not item:
        flash(u'不存在该项目。', 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_archive = True
        item_title = item.title or item.link
        db.session.add(item)
        db.session.commit()
        flash(u'「{} 」已被存档，将不会在首页显示。'.format(item_title), 'info')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/unarchive/<id>')
@login_required
def unarchive(id):
    item = Item.query.filter(Item.user == current_user, Item.id == id).first()
    if not item:
        flash(u'不存在该条目。', 'warning')
        return redirect(request.args.get('next') or url_for('.index'))
    else:
        item.is_archive = False
        item_title = item.title or item.link
        db.session.add(item)
        db.session.commit()
        flash(u'「{} 」被解除存档，将会在首页显示。'.format(item_title), 'info')
        return redirect(request.args.get('next') or url_for('.index'))


@main.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Item.query.filter(Item.user == current_user, Item.id == id).first()
    if not item:
        flash(u"不存在该条目。", 'warning')
        return redirect(url_for('.index'))
    form = EditItemForm()
    if form.validate_on_submit():
        # todo: is there a nicer solution?
        item.tags = []
        item.title = form.title.data
        if form.tags.data:
            tags = form.tags.data.split(',')
            for tag in tags:
                if Tag.query.filter_by(name=tag).first():
                    item.tags.append(Tag.query.filter_by(name=tag).first())
                else:
                    item.tags.append(Tag(name=tag))
        db.session.add(item)
        db.session.commit()
        # parse_html(item.id)
        flash(u'「{} 」，此条目已更新。'.format(item.title or item.link), 'info')
        return redirect(request.args.get('next') or url_for('.index'))
    form.title.data = item.title
    form.tags.data = ','.join([tag.name for tag in item.tags])
    return render_template('edit.html', form=form)


@main.route('/settings/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'新密码已设置。', 'success')
            return redirect(url_for('.index'))
        else:
            flash(u'原密码有误，请重新输入。', 'warning')
    return render_template('settings/change-password.html', form=form)


@main.route('/settings/drop-all', methods=['GET', 'POST'])
@login_required
def drop_all():
    form = DropAllForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            items = current_user.items
            current_user.items = []
            for item in items:
                db.session.delete(item)
            db.session.add(current_user)
            db.session.commit()
            flash(u'您已清空所有条目。', 'danger')
            return redirect(url_for('.index'))
        else:
            flash(u'您输入的密码不正确！', 'warning')
    flash(u'注意：您将会清空所有条目，此操作不可逆！', 'danger')
    return render_template('settings/drop-all.html', form=form)