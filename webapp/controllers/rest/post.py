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

