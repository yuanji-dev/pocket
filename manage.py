from app import create_app, db
from app.models import User, Item, Tag
from config import DevelopmentConfig
from flask.ext.script import Manager, Shell

app = create_app(DevelopmentConfig)

manager = Manager(app)


@manager.command
def runserver():
    app.run()


def make_shell_context():
    return dict(app=app, db=db, User=User, Item=Item, Tag=Tag)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
