# -*- coding: utf-8 -*-
from models import Item
from app import db
from config import Config
import urllib2
import json
from threading import Thread
from flask import current_app


def async_parse_html(app, id):
    with app.app_context():
        readability_api_url = Config.READABILITY_API_URL
        readability_token = Config.READABILITY_TOKEN
        item = Item.query.filter_by(id=id).first()
        print item.id, item.link
        full_url = readability_api_url.format(item.link, readability_token)
        try:
            req = urllib2.urlopen(full_url)
            res = req.read()
            parsed_item = json.loads(res)
            item.domain = parsed_item['domain']
            item.title = parsed_item['title']
            item.image = parsed_item['lead_image_url']
            item.author = parsed_item['author']
            item.content = parsed_item['content']
            db.session.add(item)
            db.session.commit()
        except:
            # todo use user-friendly error handler.
            print 'urllib2 error'


def parse_html(id):
    app = current_app._get_current_object()
    thr = Thread(target=async_parse_html, args=[app, id])
    thr.start()
    # return thr