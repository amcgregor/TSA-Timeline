#!/usr/bin/env python
# encoding: utf-8

from model import *

if __name__ == '__main__':
    # Seed data.
    Feed(name="eff-official", title="The Electronic Frontier Foundation", site="http://www.eff.org/", url="https://www.eff.org/rss/updates.xml", search=FeedSearch(attribute="title", value="TSA")).save()
    Feed(name="schneier-official", title="Schneier on Security", site="http://www.schneier.com/", url="http://feeds.feedburner.com/schneier/excerpts", search=FeedSearch(attribute="title", value="TSA")).save()
    Feed(name="tsa-official", title="The TSA Blog", site="http://www.tsa.gov/", url="http://blog.tsa.gov/feeds/posts/default?alt=rss", enabled=True).save()
