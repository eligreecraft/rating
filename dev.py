import os
from datetime import datetime

import vk

import paginator

access_token = os.getenv("VKTOKEN")
v = "5.131"
group_id = -218081274

api = vk.API(access_token=access_token, v=v)

posts = paginator.get_all_posts(api, group_id)

print(len(posts))

counter = 0

for post in posts:
    print(datetime.fromtimestamp(post["date"]))
    print(paginator.get_all_likes(api, group_id, post["id"]))
    print(paginator.get_all_comments(api, group_id, post["id"]))
    print(paginator.get_all_reposts(api, group_id, post["id"]))
    counter += 1

    if counter > 3:
        break

print(len(posts))
