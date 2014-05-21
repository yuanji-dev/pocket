# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from models import User

main = Blueprint('index', __name__)


@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)