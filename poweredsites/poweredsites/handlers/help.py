# -*- coding: utf-8 -*-
#
# Copyright(c) 2010 poweredsites.org
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tornado.web import HTTPError

from poweredsites.libs.handler import BaseHandler
from poweredsites.libs.decorators import cache

class HelpHandler(BaseHandler):
    @cache.page(anonymous=True)
    def get(self, slug=""):
        if slug == "":
            slug = "about"
        elif slug == "about":
            self.redirect("/help")
            return

        entry = self.db.get("SELECT entries.*,user.username,user.openid_name "
                            "FROM entries,user WHERE entries.user_id = user.id and slug = %s", slug)
        entries = self.db.query("SELECT * FROM entries WHERE is_help = 1")
        if not entry: raise HTTPError(404)

        self._context.title = entry.title
        self._context.keywords = ",".join((entry.title, self._context.keywords))
        self._context.description = ",".join((entry.title, self._context.description))
        self._context.is_help = True

        self.render("help.html", entry=entry, entries=entries)


handlers = [(r"/help", HelpHandler),
            (r"/help/([a-z]{2,20})", HelpHandler),
            ]
