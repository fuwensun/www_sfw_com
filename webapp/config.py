import datetime
from celery.schedules import crontab


class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'

    #my add
    # SERVER_NAME = "sfw_web_server"

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sunfuwen@127.0.0.1/www_sfw_com_db"

    #my add
    # SERVER_NAME = "sfw_web_server_prod"

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sunfuwen@127.0.0.1/www_sfw_com_db"
    # SQLALCHEMY_ECHO = True

    # ------------------------------
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"   #************becarefore*********

    # CELERY_BROKER_URL  = "redis://localhost:6379//"
    # CELERY_BACKEND_URL = "redis://localhost:6379//"
    # CELERY_RESULT_BACKEND= "redis://localhost:6379//"

    CELERY_IMPORTS = ("webapp.tasks")
    # ------------------------------

    CELERYBEAT_SCHEDULE = {

        'test--log-every-1-seconds': {
            'task': 'tasks.digest',
            'schedule': datetime.timedelta(seconds=10000),
            # 'schedule': crontab(minute=0, hour=0),
            'args': ("Message",)
        },

        'log-every-1000-seconds': {
            'task': 'webapp.tasks.log',
            'schedule': datetime.timedelta(seconds=1000),
            # 'schedule': crontab(minute=0, hour=0),
            'args':("Message",)
        },

        'weekly-digest': {
            'task': 'tasks.digest',
            'schedule': crontab(day_of_week=6, hour='10')
        },
    }

    #my add
    # SERVER_NAME = "sfw_web_server_dev"




