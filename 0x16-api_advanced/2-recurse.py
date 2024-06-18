#!/usr/bin/python3
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
        Recursively query the Reddit API and return
        a list of titles of all hot articles for a given subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'my-custom-agent/0.0.1'}
    params = {'limit': 100, 'after': after}
    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get('data', {})
    children = data.get('children', [])

    if not children:
        return hot_list if hot_list else None

    for child in children:
        hot_list.append(child['data']['title'])

    after = data.get('after')
    if after is None:
        return hot_list
    else:
        return recurse(subreddit, hot_list, after)
