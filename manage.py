from app import create_app, db
from app.models import User, Item, Tag
from config import DevelopmentConfig
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(DevelopmentConfig)

manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def runserver():
    app.run()


def make_shell_context():
    return dict(app=app, db=db, User=User, Item=Item, Tag=Tag)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
