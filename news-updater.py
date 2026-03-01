#!/usr/bin/env python3
"""Background script that fetches RSS feeds and saves as static JSON files."""

import json
import os
import time
import urllib.request
import xml.etree.ElementTree as ET

OUTPUT_DIR = '/home/user/easy-life/api/news'

RSS_FEEDS = {
    'all': [
        'https://www.mk.co.kr/rss/30100041/',
        'https://www.hankyung.com/feed/all-news',
    ],
    'stock': [
        'https://www.mk.co.kr/rss/30200030/',
    ],
    'economy': [
        'https://www.hankyung.com/feed/economy',
        'https://www.mk.co.kr/rss/30100041/',
    ],
    'crypto': [
        'https://www.mk.co.kr/rss/30100041/',
    ],
    'realestate': [
        'https://www.mk.co.kr/rss/30300018/',
        'https://www.hankyung.com/feed/realestate',
    ],
}


def fetch_rss(url):
    items = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        root = ET.fromstring(data)

        feed_title = ''
        channel = root.find('channel')
        if channel is not None:
            t = channel.find('title')
            if t is not None:
                feed_title = t.text or ''

        for item in root.iter('item'):
            title = item.findtext('title', '').strip()
            link = item.findtext('link', '').strip()
            pub_date = item.findtext('pubDate', '').strip()
            author = item.findtext('author', '').strip()
            desc = item.findtext('description', '').strip()

            thumbnail = ''
            for child in item:
                if 'content' in child.tag.lower() and child.get('url'):
                    thumbnail = child.get('url')
                    break

            if title and link:
                items.append({
                    'title': title,
                    'link': link,
                    'pubDate': pub_date,
                    'author': author or feed_title,
                    'description': desc[:200],
                    'thumbnail': thumbnail,
                })
    except Exception as e:
        print(f'  Error fetching {url}: {e}')
    return items


def update_category(category, feed_urls):
    all_items = []
    for url in feed_urls:
        all_items.extend(fetch_rss(url))

    seen = set()
    unique = []
    for item in all_items:
        key = item['title'][:40]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    filepath = os.path.join(OUTPUT_DIR, f'{category}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False)

    print(f'  {category}: {len(unique)} articles saved')


def update_all():
    print(f'[{time.strftime("%H:%M:%S")}] Updating news feeds...')
    for category, feeds in RSS_FEEDS.items():
        update_category(category, feeds)
    print(f'[{time.strftime("%H:%M:%S")}] Done.\n')


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print('News updater started. Refreshing every 60 seconds.')
    while True:
        update_all()
        time.sleep(60)
