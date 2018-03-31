from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

class User(db.Model):
    __tablename__ = "user_table_name"
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self,username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


if __name__ == '__main__':
    app.run()
