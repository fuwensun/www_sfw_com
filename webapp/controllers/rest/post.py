import datetime
from flask_restful import Resource, fields, marshal_with
from flask import abort
from webapp.models import Post, User, Tag, db, debug
from .fields import HTMLField

from .parsers import (
    post_get_parser,
    post_post_parser,
    post_put_parser,
    post_delete_parser
)



nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'id': fields.Integer(),
    'author': fields.String(attribute=lambda x: x.user.username),
    # 'author': fields.String(attribute=lambda x: x),
    'title': fields.String(),
    'text': HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_date': fields.DateTime(dt_format='iso8601')
}


class PostApi(Resource):
    @marshal_with(post_fields)

    def get(self, post_id=None):
        if post_id:
            debug(str(post_id))
            post = Post.query.get(post_id)
            # users = User.query.all()
            # debug(str(post) + str(post.user) + str(post.user_id))
            # for u in users:
            #     debug(str(u) + str(u.id))
            if not post:
                abort(404)

            return post
        else:
            # http: // 127.0.0.1: 5000 / api / post / 0?page = 1
            # http: // 127.0.0.1: 5000 / api / post / 0?page = 1 & & user = sfw
            debug("bad post_id!!!" + str(post_id))
            args = post_get_parser.parse_args()
            debug(str(args))
            page = args['page'] or 1
            debug(str(page))
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)

                posts = user.posts.order_by(
                    Post.publish_date.desc()
                ).paginate(page, 30)
            else:
                posts = Post.query.order_by(
                    Post.publish_date.desc()
                ).paginate(page, 30)

            return posts.items


    def post(self, post_id=None):
        if post_id:
            abort(400)
        else:
            # curl - d "title=From Rest" - d "text=The body text from Rest" - d "tags=Python" http: // 127.0.0.1: 5000 / api / post
            # curl - d "username=sfw" - d "password=sunfuwen" http:// 127.0.0.1: 5000 / api / auth
            # curl - d "title=From Rest" - d "text=The body text from Rest" - d "tags=Python" - d "token=eyJleHAiOjE1MjQ0NjI1NTQsImFsZyI6IkhTMjU2IiwiaWF0IjoxNTIzODU3NzU0fQ.eyJpZCI6MX0.5JT5R1g5lHFhE_7Y54NQP8oahypGHyT5yXgTNz_5kN4"http: // 127.0.0.1: 5000 / api / post
            args = post_post_parser.parse_args(strict=True)

            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)

            new_post = Post(args['title'])
            new_post.user = user
            new_post.date = datetime.datetime.now()
            new_post.text = args['text']

            if args['tags']:
                for item in args['tags']:
                    tag = Tag.query.filter_by(title=item).first()

                    # Add the tag if it exists. If not, make a new tag
                    if tag:
                        new_post.tags.append(tag)
                    else:
                        new_tag = Tag(item)
                        new_post.tags.append(new_tag)

            db.session.add(new_post)
            db.session.commit()
            return new_post.id, 201


    def put(self, post_id=None):
        # curl - X PUT - d "title=Modified From Rest" - d "text=The body text from Rest" - d "tags=Python" - d "token=eyJleHAiOjE1MjQ0NjI1NTQsImFsZyI6IkhTMjU2IiwiaWF0IjoxNTIzODU3NzU0fQ.eyJpZCI6MX0.5JT5R1g5lHFhE_7Y54NQP8oahypGHyT5yXgTNz_5kN4"http: // 127.0.0.1: 5000 / api / post / 101
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_put_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        if user != post.user:
            abort(403)

        if args['title']:
            post.title = args['title']

        if args['text']:
            post.text = args['text']

        if args['tags']:
            for item in args['tags']:
                tag = Tag.query.filter_by(title=item).first()

                # Add the tag if it exists. If not, make a new tag
                if tag:
                    post.tags.append(tag)
                else:
                    new_tag = Tag(item)
                    post.tags.append(new_tag)

        db.session.add(post)
        db.session.commit()
        return post.id, 201

    def delete(self, post_id=None):
        # curl - X DELETE - d "token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMzg1OTMxMywiZXhwIjoxNTI0NDY0MTEzfQ.eyJpZCI6MX0.e62uRCtdy0J3n2whNpkWiHkwNdaufJVsX7Fxhkw5zQY" http: // 127.0.0.1: 5000 / api / post / 101
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if user != post.user:
            abort(401)

        db.session.delete(post)
        db.session.commit()
        return "", 204

