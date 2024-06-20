#!/usr/bin/python3
"""
    Recursively query the Reddit API,
    parse titles of all hot articles,
    and print a sorted count of given keywords.
"""
from collections import Counter
import requests


def count_words(subreddit, word_list, after=None, word_counter=None):
    """
        Recursively query the Reddit API,
        parse titles of all hot articles,
        and print a sorted count of given keywords.
    """
    if word_counter is None:
        word_counter = Counter()

    normalized_word_list = [word.lower() for word in word_list]
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'my-custom-agent/0.0.1'}
    params = {'limit': 100, 'after': after}
    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get('data', {})
    children = data.get('children', [])

    for child in children:
        title = child['data']['title'].lower()
        words_in_title = title.split()
        for word in words_in_title:
            cleaned_word = ''.join(filter(str.isalpha, word))
            if cleaned_word in normalized_word_list:
                word_counter[cleaned_word] += 1

    after = data.get('after')
    if after is not None:
        count_words(subreddit, word_list, after, word_counter)
    else:
        if word_counter:
            sorted_word_count = sorted(
                    word_counter.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_word_count:
                print(f"{word}: {count}")
