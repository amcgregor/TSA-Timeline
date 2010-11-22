#!/usr/bin/env python
# encoding: utf-8

from model import *

if __name__ == '__main__':
    # Clear data.
    
    Feed.drop_collection()
    Story.drop_collection()
    
    # Seed data.
    Feed(name="eff-official", title="The Electronic Frontier Foundation", site="http://www.eff.org/", url="https://www.eff.org/rss/updates.xml", search=FeedSearch(attribute="title", value="TSA"), enabled=True).save()
    Feed(name="schneier-official", title="Schneier on Security", site="http://www.schneier.com/", url="http://feeds.feedburner.com/schneier/excerpts", search=FeedSearch(attribute="title", value="TSA"), enabled=True).save()
    Feed(name="tsa-official", title="The TSA Blog", site="http://www.tsa.gov/", url="http://blog.tsa.gov/feeds/posts/default?alt=rss", enabled=True).save()
    Feed(name="google-news", title="Google News", site="http://news.google.com/", url="http://news.google.ca/news?hl=en&rls=en&q=TSA&um=1&ie=UTF-8&output=rss", enabled=True).save()
