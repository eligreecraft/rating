import os
from collections import Counter

import vk
from tqdm import tqdm

import paginator
import view
from model import Report
from used import USED

# Todo - CI

access_token = os.getenv("VKTOKEN")
v = "5.131"
group_id = -218081274
ignored_ids = {3159776, 90460059, 495748987}

api = vk.API(access_token=access_token, v=v)

posts = paginator.get_all_posts(api, group_id)

liker_ids = []
commenter_ids = []

# Лайк - 1 балл
like_ball_count = 1
# Комент - 3 балла
comment_ball_count = 3

ball_ids = []

uid_to_name = {}
uid_to_url = {}

for post in tqdm(posts):
    post_id = post["id"]

    likes = paginator.get_all_likes(api, group_id, post_id)
    liker_ids.extend(likes)
    for _ in range(like_ball_count):
        ball_ids.extend(likes)

    comments = paginator.get_all_comments(api, group_id, post_id)
    commenter_ids.extend(comments)
    for _ in range(comment_ball_count):
        ball_ids.extend(comments)

ball_ids = list(filter(lambda x: x > 0, ball_ids))

like_counter = Counter(liker_ids)
comment_counter = Counter(commenter_ids)
ball_ids = Counter(ball_ids)

users = api.users.get(
    user_ids=ball_ids.keys(),
    fields=[
        "screen_name",
    ],
)

report = Report()

for user in users:
    uid_to_name[user["id"]] = f"{user['first_name']} {user['last_name']}"
    uid_to_url[user["id"]] = f"https://vk.com/{user['screen_name']}"

for (uid, count) in ball_ids.most_common():
    print(uid, uid_to_url[uid])

    if uid in ignored_ids:
        continue

    name = uid_to_name[uid]
    url = uid_to_url[uid]
    likes = like_counter.get(uid) if like_counter.get(uid) else 0
    comments = comment_counter.get(uid) if comment_counter.get(uid) else 0
    balls = ball_ids[uid]

    report.add(
        name=name,
        url=url,
        likes=likes,
        comments=comments,
        balls=balls,
        used=USED.get(uid),
    )

view.build(report)
