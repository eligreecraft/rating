import itertools
import time

import vk

SLEEP_TIME = 2

POST_COUNT = 100
LIKE_COUNT = 1000
COMMENT_COUNT = 100
REPOST_COUNT = 1000


def _get_all(
    method,
    count: int,
    owner_id: int,
    item_id: int = None,
    type: int = None,
    post_id: int = None,
):
    items = []
    offset = 0

    while True:
        result = method(
            owner_id=owner_id,
            item_id=item_id,
            post_id=post_id,
            count=count,
            offset=offset,
            type=type,
        )

        if len(result["items"]) > 0:
            items.extend(result["items"])
        else:
            break

        offset = offset + count
        time.sleep(SLEEP_TIME)

    return items


def get_all_posts(api: vk.API, owner_id: int):
    return _get_all(api.wall.get, POST_COUNT, owner_id)


def get_all_likes(api: vk.API, owner_id: int, item_id: int):
    return _get_all(
        api.likes.getList, POST_COUNT, owner_id, item_id=item_id, type="post"
    )


def _get_all_comments_with_duplicates(api: vk.API, group_id: int, post_id: int):
    return list(
        map(
            lambda x: x["from_id"],
            _get_all(api.wall.getComments, COMMENT_COUNT, group_id, post_id=post_id),
        )
    )


def _dedup_adjacent(list_):
    return [k for k, g in itertools.groupby(list_)]


def get_all_comments(api: vk.API, owner_id: int, post_id: int):
    return _dedup_adjacent(_get_all_comments_with_duplicates(api, owner_id, post_id))
