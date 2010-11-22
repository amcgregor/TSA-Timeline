#!/usr/bin/env python
# encoding: utf-8

import logging

import web.core

from model import *


log = logging.getLogger(__name__)



class RootController(web.core.Controller):
    def index(self):
        return 'Hello world!'

    def hello(self, name):
        return "Hello, %(name)s!" % dict(name=name)



if __name__ == '__main__':
    from paste import httpserver
    
    logging.basicConfig(level=logging.INFO)
    
    app = web.core.Application.factory(root=RootController, debug=False, **{
            "web.sessions": False,
            "web.cache": False,
            "web.static": True,
            "web.compress": True,
            "web.templating.engine": "mako",
        })
    
    httpserver.serve(app, host='127.0.0.1', port='8080')
