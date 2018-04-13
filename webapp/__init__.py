from flask import Flask, redirect, url_for
from webapp.config import DevConfig
from webapp.models import db
from webapp.controllers.blog import blog_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint)

    return app


app = create_app(DevConfig)
# app = create_app('webapp.config.ProdConfig')

if __name__ == '__main__':
    app.run()
