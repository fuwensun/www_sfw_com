from flask_restful import Resource

class PostApi(Resource):
    def get(self,post_id=None):
        if post_id:
            return{'id':post_id}
        return {'hello':'world'}