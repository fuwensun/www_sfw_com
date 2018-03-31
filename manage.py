from flask_script import Manager,Server
from main import app, db, User, Post

manager = Manager(app)

manager.add_command("Server",Server())

@manager.shell

def make_shell_context():
    return dict(app = app, db = db, User = User, Post = Post)






#-----------------------
#
# from manage import *
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
# page = User.query.paginate(1,1)
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