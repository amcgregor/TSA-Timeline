#!/usr/bin/env python
# encoding: utf-8

import pytz
import logging

from time import mktime
from datetime import datetime
from feedparser import parse

from model import *
from mongoengine import ValidationError


log = logging.getLogger(__name__)


def tdt(ts):
    return datetime.fromtimestamp(mktime(ts))


def main():
    for feed in Feed.objects(enabled=True).order_by('-updated'):
        log.info("Updating %s...", feed.title)
        
        try:
            d = parse(feed.url)
            
            if feed.updated and d.feed.get('updated_parsed', None) and tdt(d.feed.get('updated_parsed', None)) < feed.updated:
                log.warn("Feed hasn't been updated, skipping.")
                continue
            
            feed.title = d.feed.title
            feed.site = d.feed.link
            
            if feed.updated:
                new = [article for article in d.entries if article.get('date_parsed', None) and tdt(article.get('date_parsed', None)) > feed.updated]
            
            else:
                new = d.entries
            
            log.info("Found %d articles, %d new.", len(d.entries), len(new))
            
            saved = 0
            for article in new:
                if feed.search:
                    if feed.search.value[1] == '!' and feed.search.value.lower() in getattr(article, feed.search.attribute, '').lower():
                        continue
                    
                    if feed.search.value[0] != '!' and feed.search.value.lower() not in getattr(article, feed.search.attribute, '').lower():
                        continue
                
                try:
                    Story(
                            feed = feed,
                            date = tdt(article.date_parsed),
                            # entry = article,
                            url = article.link,
                            title = article.title,
                            description = article.get('description', None)
                        ).save()
                
                except ValidationError:
                    log.error("Validation error in article: %r", article)
                    raise
                
                saved += 1
            
            log.info("%d articles matched critera.", saved)
            
            if d.get('updated_parsed', None):
                feed.updated = tdt(article.date_parsed)
            else:
                feed.updated = datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc)
            
            feed.save(safe=False)
        
        except:
            log.exception("Error updating feed.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
