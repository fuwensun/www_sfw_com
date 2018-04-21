import os
import datetime
import random

from flask_script import Manager,Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand
from webapp import create_app
from webapp.models import db, User, Role, Post, Tag, tags,Comment
from webapp.config import DevConfig
from webapp.tasks import log,multiply,remind,digest,m

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
myapp = create_app('webapp.config.%sConfig' % env.capitalize())
# myapp = create_app(DevConfig)

migrate = Migrate(myapp,db)

manager = Manager(myapp)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())
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
        multiply = multiply,
        remind = remind,
        digest = digest,
        m = m,
    )

@manager.command
def setup_db():
    db.create_all()

    admin_role = Role(name = "admin")
    admin_role.description = "admin"
    db.session.add(admin_role)

    default_role = Role(name = "default")
    default_role.description = "default"
    db.session.add(default_role)

    admin = User(username = "admin")
    admin.set_password("password")
    admin.roles.append(admin_role)
    admin.roles.append(default_role)
    db.session.add(admin)

    tag_one = Tag('Python')
    tag_two = Tag('Flask')
    tag_three = Tag('SQLAlechemy')
    tag_four = Tag('Jinja')
    tag_list = [tag_one, tag_two, tag_three, tag_four]

    s = "Body text"

    for i in range(100):
        new_post = Post("Post " + str(i))
        new_post.user = admin
        new_post.publish_date = datetime.datetime.now()
        new_post.text = s
        new_post.tags = random.sample(tag_list, random.randint(1, 3))
        db.session.add(new_post)

    db.session.commit()


if __name__ == "__main__":
    manager.run()

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
# delete from comment where id between 38 and 62;
# delete from comment where id  not between 0 and 100;
#
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


# --------<celery 使用>-----------
#
# --rabbitmq使用--
# echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
# wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
# sudo apt-get install rabbitmq-server
# sudo apt-get update
# sudo apt-get install rabbitmq-server
#
# sudo rabbitmq-server
# ps aux | grep rabbitmq
# invoke-rc.d rabbitmq-server status
# invoke-rc.d rabbitmq-server start
# invoke-rc.d rabbitmq-server restart
# invoke-rc.d rabbitmq-server stop
#
# --redis使用--
# sudo apt-get install redis-server
# sudo /etc/init.d/redis-server status
# sudo /etc/init.d/redis-server restart
# sudo /etc/init.d/redis-server status
# netstat -nlt|grep redis

#--------<celery cmd>---------
# celery worker -A celery_runner --loglevel=info
# celery worker -A celery_runner --loglevel=info --config=celery_config
#
# from webapp.tasks import log
# log("Message")
# result = log.delay("Message")
# result.ready()
# result.get()
#ALT + SHIFT + INS ---》 CLOUMN EDIT
#-------
# celery status
# ps -ef |grep celery |awk '{print $2}'|xargs kill -9
# celery status
# celery control shutdown celery@ud30g_u1
# celery inspect state
# celery inspect stats
# celery inspect clock
# celery inspect conf
# celery inspect ping
# celery inspect report
#-------
# a = multiply.subtask((4,4),countdown=1)
# a.ready()
# log(2)
# log.delay(5)
# multiply(4,5)
# multiply.delay(4,5)
# multiply.s(4,5)
# multiply.s(4,5)()
# multiply.s(4,5).delay()
# multiply.apply_async((4,4),link=log.s())
# multiply.apply_async((4,49),link=log.si("message"))
# partial = multiply.s(2)
# partial.delay(3)
# partial = multiply.s(2).delay(7)
# multiply.apply_async((4,49),link=multiply.s(4))
# multiply.apply_async((4,49),link=multiply.s(4)).get()
# multiply.apply_async((4,49),link=multiply.s(4)).ready()
# from celery import group
# sig = group(multply.s(i,i+5) for i in range(10))
# result = sig.delay()
# result.get()
# from celery import chain
# sig = chain(multiply.s(10,10), multiply.s(4), multiply.s(20))
# result = sig.delay()
# result.get()
# a = multiply.apply_async((4,49),link=multiply.s(4))
# a.get()
# a multiply.apply_async((4,49),link=log.si("message"))
# a = multiply.apply_async((4,49),link=log.si("message"))
# a.get()
# from celery.schedules import crontab
# crontab(minute=0,hour=0)