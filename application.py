#!/usr/bin/env python
# encoding: utf-8

import logging

import web.core

from model import *


log = logging.getLogger(__name__)



class RootController(web.core.Controller):
    def index(self, p=1, pp=5):
        """Display the 10 latest articles."""
        p = int(p)
        pp = int(pp)
        return './templates/list.html', dict(Feed=Feed, Story=Story, maximum=10, page=p, pp=pp)
    
    def archive(self, p=1, pp=5):
        p = int(p)
        pp = int(pp)
        return './templates/list.html', dict(Feed=Feed, Story=Story, maximum=10, page=p, pp=pp)
    
    def feeds(self, feed=None):
        """Display a list of feeds or details about one feed."""
        if feed:
            return './templates/feed.html', dict(Feed=Feed, Story=Story, feed=feed)
        
        return './templates/feeds.html', dict(Feed=Feed, Story=Story)
    
    def stats(self):
        """Display site statistics."""
        return './templates/stats.html', dict(Feed=Feed, Story=Story)
    
    # Static views.
    
    def about(self):
        return './templates/about.html', dict()
    
    def privacy(self):
        return './templates/privacy.html', dict()



if __name__ == '__main__':
    import sys
    from paste import httpserver
    
    logging.basicConfig(level=logging.INFO)
    
    app = web.core.Application.factory(root=RootController, debug=False, **{
            "web.sessions": False,
            "web.cache": False,
            "web.static": True if len(sys.argv) < 2 else False, # production check
            "web.compress": True if len(sys.argv) < 2 else False, # production check
            "web.templating.engine": "mako",
        })
    
    httpserver.serve(app, host='127.0.0.1', port='8080' if len(sys.argv) < 2 else sys.argv[1])
