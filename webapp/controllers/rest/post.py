from flask_restful import Resource, fields, marshal_with
from flask import abort
from webapp.models import Post
from .fields import HTMLField

post_fields = {
    'title': fields.String(),
    'text':HTMLField(),
    'publish_date':fields.DateTime(dt_format='iso8601')
}

class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self,post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            return post
        else:
            posts = Post.query.all()
            return posts
