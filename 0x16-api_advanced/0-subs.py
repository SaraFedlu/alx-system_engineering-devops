#!/usr/bin/python3
''' Extract number of subscribers on reddit'''
import requests


def number_of_subscribers(subreddit):
    ''' Function for achieving the script purpose'''
    # Reddit API URL for getting subreddit information
    url = f"https://www.reddit.com/r/{subreddit}/about.json"

    # Set a custom User-Agent header to avoid Too Many Requests error
    headers = {'User-Agent': 'linux/firefox-sarah'}

    # Send GET request to Reddit API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Extract number of subscribers
        subscribers = data['data']['subscribers']
        return subscribers
    else:
        # If the subreddit is invalid or any other error occurred, return 0
        return 0
