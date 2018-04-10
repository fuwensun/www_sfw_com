import random
import datetime
from main import *


user = User.query.get(1)
tag_one = Tag('Python')
tag_two = Tag('Flask')
tag_three = Tag('SQLAlechemy')
tag_four = Tag('JinJa')
tag_list = [tag_one,tag_two,tag_three,tag_four]

s = "Example text"

for i in range(100):
    new_post = Post("Post " + str(i))
    new_post.user = user
    new_post.publish_date = datetime.datetime.now()
    new_post.text = s
    new_post.tag = random.sample(tag_list, random.randint(1,3))
    db.session.add(new_post)

db.session.commit()