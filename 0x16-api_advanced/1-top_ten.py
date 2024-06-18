#!/usr/bin/python3
"""
    Query the Reddit API and
    print the titles of the first 10 hot posts for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """
        Query the Reddit API and
        print the titles of the first 10 hot posts for a given subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'my-custom-agent/0.0.1'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        for post in posts:
            print(post['data']['title'])
    else:
        print(None)
