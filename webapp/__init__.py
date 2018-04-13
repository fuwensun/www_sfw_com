from flask import Flask, redirect, url_for
from webapp.config import DevConfig
from webapp.models import db
from webapp.extensions import bcrypt, oid
from webapp.controllers.blog import blog_blueprint
from webapp.controllers.main import main_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    oid.init_app(app)

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)

    return app


app = create_app(DevConfig)
# app = create_app('webapp.config.ProdConfig')

if __name__ == '__main__':
    app.run()
