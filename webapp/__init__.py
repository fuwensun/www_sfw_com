import os
from flask import Flask, redirect, url_for
from webapp.config import DevConfig
from webapp.models import db
from webapp.controllers.blog import blog_blueprint
from webapp.controllers.main import main_blueprint
from webapp.controllers.rest.post import PostApi
from webapp.controllers.rest.auth import AuthApi
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user

from webapp.extensions import (
    bcrypt,
    oid,
    login_manager,
    principals,
    rest_api,
    celery
)


def debug(str):
    print("<=== my debug ===> " + str)

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    celery.init_app(app)

    # debug("celery.conf" + '-----' + str(celery._preconf['result_backend']))
    debug(str(celery._preconf.items()))

    rest_api.add_resource(
        AuthApi,
        '/api/auth',
    )

    rest_api.add_resource(
        PostApi,
        '/api/post',
        '/api/post/<int:post_id>',
    )

    rest_api.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

        debug("on_identity_loaded()" + '-----' + str(current_user))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)
    return app

if __name__ == '__main__':
    env = os.environ.get('WEBAPP_ENV', 'dev')
    myapp = create_app('webapp.config.%sConfig' % env.capitalize())
    # myapp = create_app(DevConfig)
    myapp.run()
