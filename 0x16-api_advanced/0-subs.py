#!/usr/bin/python3
"""
    Query the Reddit API and
    return the number of subscribers for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """
        Query the Reddit API and
        return the number of subscribers for a given subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {'User-Agent': 'my-custom-agent/0.0.1'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 404:
        return 0
    else:
        data = response.json().get("data")
        return data.get("subscribers")
