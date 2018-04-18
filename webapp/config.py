
class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sunfuwen@127.0.0.1/www_sfw_com_db"

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sunfuwen@127.0.0.1/www_sfw_com_db"
    SQLALCHEMY_ECHO = True

    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"   #************becarefore*********

    # CELERY_BROKER_URL  = "redis://localhost:6379//"
    # CELERY_BACKEND_URL = "redis://localhost"

    CELERY_IMPORTS = ("webapp.tasks")




