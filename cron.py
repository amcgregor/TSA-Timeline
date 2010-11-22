#!/usr/bin/env python
# encoding: utf-8

import pytz
import logging

from time import mktime
from datetime import datetime
from feedparser import parse

from model import *


log = logging.getLogger(__name__)



def main():
    for feed in Feed.objects(enabled=True).order_by('-updated'):
        log.info("Updating %s...", feed.title)
        
        try:
            d = parse(feed.url)
            
            if d.feed.get('updated_parsed', None) and d.feed.get('updated_parsed', None) < feed.updated:
                log.warn("Feed hasn't been updated, skipping.")
                continue
            
            feed.title = d.feed.title
            feed.site = d.feed.link
            
            if feed.updated:
                new = [article for article in d.entries if datetime.fromtimestamp(mktime(article.date_parsed)) > feed.updated]
            
            else:
                new = d.entries
            
            log.info("Found %d articles, %d new.", len(d.entries), len(new))
            
            saved = 0
            for article in new:
                if feed.search:
                    if feed.search.value.lower() not in article.title.lower():
                        continue
                
                Story(
                        feed = feed,
                        date = datetime.fromtimestamp(mktime(article.date_parsed)),
                        # entry = article,
                        url = article.link,
                        title = article.title,
                        description = article.get('description', None)
                    ).save()
                saved += 1
            
            log.info("%d articles matched critera.", saved)
            
            if d.get('updated_parsed', None):
                feed.updated = datetime.fromtimestamp(mktime(article.date_parsed))
            else:
                feed.updated = datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc)
            
            feed.save(safe=False)
        
        except:
            log.exception("Error updating feed.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
