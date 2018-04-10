from flask_script import Manager,Server
from main import app, db, User, Post, Tag, tags,Comment
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app,db)

manager = Manager(app)

manager.add_command("Server",Server())

manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app, db = db, User = User, Post = Post, Tag = Tag, tags = tags,Comment = Comment)

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