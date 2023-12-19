import requests
import json
import markovify
from pprint import pprint
import re
import html
import time

API_BASE = "https://hacker-news.firebaseio.com/v0/"



class Item(dict):
    def __init__(self, itemid):
        # Retrieve the item from HackerNews API
        r = requests.get(f"{API_BASE}/item/{itemid}.json")
        self.update(json.loads(r.content))


def ensure_item(itm):
    if isinstance(itm, Item):
        return itm
    else:
        return Item(itm)


def kids(itm, depth=-1):
    itm = ensure_item(itm)
    kids = itm.get('kids', [])
    return [Item(kid_id) for kid_id in kids]


def fetch_stories(sort='top'):
    """
    Retrieve a list (up to 500) of story IDs from HackerNews API

    Parameters
    ----------
    sort, optional : str
        One of `'top', 'new', 'best'`. Defaults to `'top'`
    """
    r = requests.get(f"{API_BASE}/{sort}stories.json")
    if r.ok:
        return json.loads(r.content)


def has_kids(itm):
    itm = ensure_item(itm)
    return bool(itm.get('kids', []))


def with_kids(items):
    for itm in items:
        if has_kids(itm):
            yield itm


def combine(a, b):
    if not a:
        m = b
    else:
        m = markovify.combine([a, b])

    return m


def fetch_comments(story):
    return [comment.get('text', '') for comment in kids(story)]


def munge_comment(comment):
    comment = re.sub('<[^>]+>', ' ', comment)
    comment = html.unescape(comment)
    return comment.strip()


if __name__ == "__main__":
    stories = fetch_stories('new')
    corpus = []
    for story in with_kids(stories):
        print(f"Story #{story} has comments")
        corpus += [munge_comment(c).split() for c in fetch_comments(story)]

    # corpus = [["A", "list", "of", "exploded", "sentences"], ...]
    model = markovify.Chain(corpus, state_size=3)
    with open(f'hn_markov_{time.time()}.json', 'w') as f:
        f.write(model.to_json())
