import os
from webapp.extensions import debug
from webapp import create_app
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL'],
    )
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    # debug(str(celery.conf))
    return celery

env = os.environ.get('WEBAPP_ENV', 'dev')
flask_app = create_app('webapp.config.%sConfig' % env.capitalize())
# flask_app = create_app(DevConfig)
celery = make_celery(flask_app)




# self.__autoset('result_backend', backend)
# self._preconf[key] = value
# self._preconf_set_by_auto.add(key)