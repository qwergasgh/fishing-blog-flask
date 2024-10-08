from app.models import User, Role
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app import app, db

manager = Manager(app)

migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,
                db=db, 
                User=User, 
                Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
