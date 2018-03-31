class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sunfuwen@127.0.0.1/www_sfw_com_db"
    SQLALCHEMY_ECHO = True


