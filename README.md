pocket
======

##介绍

使用[flask](http://flask.pocoo.org/)框架编写的一个类似于[Pocket(read it later)](http://getpocket.com)的web应用。

##功能

添加URL，将网页内容保存到服务器，方便以后阅读。

##Demo

[http://pocket.gimo.me](http://pocket.gimo.me)

##截图

- [screenshot1](http://ww1.sinaimg.cn/large/4b31c31egw1ei6jll3v7bj20lo0gxdhw.jpg)

- [screenshot2](http://ww1.sinaimg.cn/large/4b31c31egw1ei6jm8o5ahj20k00zk0ut.jpg)

- [screenshot3](http://ww1.sinaimg.cn/large/4b31c31egw1ei6jmggeucj20k00zk0wy.jpg)

##运行

*建议使用virtualenv*

1. `git clone https://github.com/Masakichi/pocket.git`
2. `cd pocket && pip install -r requirements.txt`
3. `python manage.py shell`
4. `db.create_all()`
5. `python manage.py runserver`

##TODO

- 添加API
- 重写html_parser
