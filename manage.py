import os
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from webapp import create_app
from webapp.models import db, User, Role, Post, Tag, tags,Comment
from webapp.config import DevConfig
from webapp.tasks import log

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
myapp = create_app('webapp.config.%sConfig' % env.capitalize())
# myapp = create_app(DevConfig)

migrate = Migrate(myapp,db)

manager = Manager(myapp)

manager.add_command("Server",Server())

manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(
        app = myapp,
        db = db,
        User = User,
        Role=Role,
        Post = Post,
        Tag = Tag,
        tags = tags,
        Comment = Comment,
        env = env,
        log = log,

    )

if __name__ == "__main__":
    manager.run()



# --celery 使用-------
# echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
# wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
# sudo apt-get install rabbitmq-server
# sudo apt-get update
# sudo apt-get install rabbitmq-server
# rabbitmq-server
# sudo rabbitmq-server
# ps aux | grep rabbit
# ps aux | grep rabbitmq
# invoke-rc.d rabbitmq-server status
#
# celery worker -A celery_runner --loglevel=info
# celery worker -A celery_runner --loglevel=info --config=celery_config
#
# from webapp.tasks import log
# log("Message")
# result = log.delay("Message")
# result.ready()
# result.get()

# celery status
# celery report
# celery inspect conf


# 1按装：
# sudo apt-get install mysql-server
# sudo apt-get install mysql-client
# sudo apt-get install libmysqlclient-dev
# sudo netstat -tap | grep mysql
#
#
# 2登入：
# mysql -u root -p
#
# 3使用库：
# show databases;
# mysqladmin -u root -p create xxxdb;
# mysqladmin -u root -p drop xxxdb;
# use xxxdb;
#
# 4使用表：
# show tables;
# create table xxxtable(column_name column_type);
# describe xxxtable;
# drop table xxxtable;
# select * from xxxtable;
#
#5
#top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by('total DESC').limit(5).all()
#-----------------------
#
# from manage import *
#
# python manage.py shell
#
# db.create_all()
#
# user = User(username='fuck_name')
#
# db.session.add(user)
#
# db.session.commit()
#
# users = User.query.all()
#
# users = User.query.limit(10).all()
#
# users = User.query.order_by(User.username).all()
#
# users = User.query.order_by(User.username.desc()).all()
#
# user = User.query.first()
#
# user.username
#
# user = User.query.get(1)
#
# user.username
#
# user = User.query.order_by(User.username.desc()).limit(10).first()

# -----------------------
#
# page = User.query.paginate(1,2)
#
# page.items
#
# page.page
#
# page.pages
#
# page.has_next
#
# page.has_prev
#
# page.next()
#
# page.prev()
#
# ----------------
#
# type(User.username.desc())
#
# User.query.filter_by(username = 'fake_name').update({'password':'test'})
#
# db.session.commit()
#
# user = User.query.filter_by(username = 'fake_name').first()
#
# db.session.delete(user)
#
# db.session.commit()
#
# -----------------
#
# user = User.query.get(1)
#
# new_post = Post('Post Title')
#
# new_post.user_id = user.id
#
# user.posts.all()
#
# db.session.add(new_post)
#
# db.session.commit()
#
# second_post = Post('Second Title')
#
# second_post.user = user
#
# db.session.add(second_post)
#
# db.session.commit()
#
# -----------------
# db.create_all()
#
# post_one = Post.query.filter_by(title = 'Post Title').first()
#
# post_one
#
# post_two = Post.query.filter_by(title = 'Second Title').first()
#
# post_two
#
# tag_one = Tag('Python')
#
# tag_two = Tag('SQLAlchemy')
#
# tag_three = Tag('Flask')
#
# post_one.tags.all()
#
# tag_two.posts.all()
#
# post_one.tags = [tag_one]
#
# post_two.tags = [tag_one, tag_two, tag_three]
#
# tag_two.posts
#
# post_one.tags.all()
#
# post_two.tags.all()
#
# tag_one.posts.all()
#
# db.session.add(post_one)
#
# db.session.add(post_two)
#
# db.session.commit()
#
# tag_one.posts.append(post_one)
#
# tag_three.posts.append(post_one)
#
# tag_three.posts.all()
#
# db.session.add(tag_three)
#
# db.session.commit()
#
# -----------------
# db.create_all()
# arole = Role('admin')
# arole.description = 'admin_role'
# prole = Role('poster')
# prole.description = 'poster_role'
# drole = Role('default')
# drole.description = 'default_role'
# db.session.add(arole)
# db.session.add(prole)
# db.session.add(drole)
# db.session.commit()

# user = User.query.filter_by(username = 'sfw').first()
#
# prole = Role.query.filter_by(username = 'poster').first()


