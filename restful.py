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

import mimeparse
from tornado.web import HTTPError

class JSONMixin:
    def head(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        if mime == "text/html":
            self.head_html(*args, **kwargs)
        elif mime == "application/json":
            self.head_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def get(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        print(mime)
        if mime == "text/html":
            self.get_html(*args, **kwargs)
        elif mime == "application/json":
            self.get_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def post(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        if mime == "text/html":
            self.post_html(*args, **kwargs)
        elif mime == "application/json":
            self.post_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def delete(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        if mime == "text/html":
            self.delete_html(*args, **kwargs)
        elif mime == "application/json":
            self.delete_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def patch(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        if mime == "text/html":
            self.patch_html(*args, **kwargs)
        elif mime == "application/json":
            self.patch_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def put(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        if mime == "text/html":
            self.put_html(*args, **kwargs)
        elif mime == "application/json":
            self.put_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def options(self, *args, **kwargs):
        mime = mimeparse.best_match(['application/json', 'text/html'],
                self.request.headers.get("Accept"))
        if mime == "text/html":
            self.options_html(*args, **kwargs)
        elif mime == "application/json":
            self.options_json(*args, **kwargs)
        else:
            raise HTTPError(405)

    def head_html(self):
        raise HTTPError(405)

    def head_json(self):
        raise HTTPError(405)

    def get_html(self):
        raise HTTPError(405)

    def get_json(self):
        raise HTTPError(405)

    def post_html(self):
        raise HTTPError(405)

    def post_json(self):
        raise HTTPError(405)

    def delete_html(self):
        raise HTTPError(405)

    def delete_json(self):
        raise HTTPError(405)

    def patch_html(self):
        raise HTTPError(405)

    def patch_json(self):
        raise HTTPError(405)

    def put_html(self):
        raise HTTPError(405)

    def put_json(self):
        raise HTTPError(405)

    def options_html(self):
        raise HTTPError(405)

    def options_json(self):
        raise HTTPError(405)

