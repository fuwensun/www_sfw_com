from flask import flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_openid import OpenID

bcrypt = Bcrypt()
oid = OpenID()


@oid.after_login
def create_or_login(resp):
    from .models import db, User
    username = resp.fullname or resp.nickname or resp.email

    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    session['username'] = username
    return redirect(url_for('blog.home'))