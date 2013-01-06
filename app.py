"""
This file is part of Vapour.

Vapour is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Vapour is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Vapour.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import json
import re
import uuid

import pymongo
import tornado.options
import tornado.web
from bson.json_util import dumps
from mako.lookup import TemplateLookup
from pymongo import Connection
from tornado.web import HTTPError, RequestHandler, StaticFileHandler

from restful import JSONMixin

class Application(tornado.web.Application):
    def __init__(self, handlers, **settings):
        tornado.web.Application.__init__(self, handlers, **settings)
        self.collection = Connection().vapour.urls
        self.templates = TemplateLookup(directories=["templates"])

    def get_link_by_id(self, id):
        record = self.collection.find_one({'_id': uuid.UUID(id)})
        return fix_id(record)

    def get_links_by_tag(self, tag):
        records = self.collection.find({'tags': re.compile(tag, re.I)})
        return fix_ids(records)

    def get_links_by_url(self, url):
        records = self.collection.find({'url': re.compile(url, re.I)})
        return fix_ids(records)

    def insert_link(self, url, desc, tags):
        return self.collection.insert({
            '_id': uuid.uuid4(),
            'url': url,
            'desc': desc,
            'tags': tags,
            'added': datetime.datetime.utcnow()
        })


def fix_id(record):
    if record is None:
        return None
    record['id'] = record['_id'].hex
    del record['_id']
    return record


def fix_ids(records):
    records = list(records)
    for i in range(len(records)):
        records[i] = fix_id(records[i])
    return records


class TagHandler(JSONMixin, tornado.web.RequestHandler):
    def get_json(self, tag):
        records = self.application.get_links_by_tag(tag)
        if records == []:
            self.set_status(404)
        self.write(dumps(records, indent=2))

    def get_html(self, tag):
        self.write("""<!DOCTYPE html><html><head><meta
        charset='utf-8'><title></title></head><body><pre>""")
        self.get_json(tag)
        self.write("</pre></body></html>")


class LinkHandler(JSONMixin, tornado.web.RequestHandler):
    def get_json(self, id):
        record = self.application.get_link_by_id(id)
        if record is None:
            set_status(404)
            record = {}
        self.write(dumps(record, indent=2))

    def put_json(self, id):
        raise HTTPError(405)

    def delete_json(self, id):
        raise HTTPError(405)

    def get_html(self, id):
        self.write("""<!DOCTYPE html><html><head><meta
        charset='utf-8'><title></title></head><body><pre>""")
        self.get_json(id)
        self.write("</pre></body></html>")

    def options(self): ...


class LinksHandler(JSONMixin, tornado.web.RequestHandler):
    def post_json(self):
        """ add new link """
        url = self.get_argument('url')
        desc = self.get_argument('desc')
        tags = [x.lstrip('#') for x in self.get_argument('tags').split(" ")]
        self.application.insert_link(url, desc, tags)

    def get_json(self):
        """ last 20 added links """
        records = [fix_id(x) for x in self.application.collection.find()
                   .sort('added', pymongo.DESCENDING).limit(20)]
        self.write(dumps(records, indent=2))

    def post_html(self):
        self.post_json()

    def get_html(self):
        self.write("""<!DOCTYPE html><html><head><meta
        charset='utf-8'><title></title></head><body><form method='post'>
        <input name='url' type='url' placeholder='URL'>
        <input name='desc' placeholder='Description'><input name='tags'
        placeholder='#tag1 #tag2 #etc'><br>
        <input type='submit'></form><br><pre>""")
        self.get_json()
        self.write("</pre></body></html>")

    def options(self): ...


class URLQueryHandler(JSONMixin, tornado.web.RequestHandler):
    def get_json(self, url=None):
        if url is None:
            return HTTPError(405)
        records = self.application.get_links_by_url(url)
        if records == []:
            self.set_status(404)
        self.write(dumps(records))

    def get_html(self, url=None):
        if url is None:
            self.write("Search by URL (soon).")
            return
        
        self.write("<pre>")
        self.get_json(url)
        self.write("</pre>")

class QueryHandler(JSONMixin, tornado.web.RequestHandler):
    def post_json(self): ...
    def get_json(self):
        ...

    def get_html(self):
        self.get_json()

    def options(self): ...


class HomePageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(self.application.templates
                .get_template("home.html").render())

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = Application([
        (r"/", HomePageHandler),
        (r"/static/(.*)", StaticFileHandler, {"path": "static"}),

        # Long forms
        (r"/tag/(.*)", TagHandler),
        (r"/query/(.*)", QueryHandler),
        (r"/links/(.*)", LinkHandler),
        (r"/links", LinksHandler),
        (r"/url/(.*)", URLQueryHandler),
        (r"/url", URLQueryHandler),

        # Short forms
        (r"/t/(.*)", TagHandler),
        (r"/q/(.*)", QueryHandler),
        (r"/l/(.*)", LinkHandler),
        (r"/l", LinksHandler),
        (r"/u/(.*)", URLQueryHandler),
        (r"/u", URLQueryHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
