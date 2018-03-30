from flask_script import Manager,Server
from mian import app

manager = Manager(app)

manager.add_command("Server",Server())

@manager.shell

def make_shell_context():
    return dict(app = app)