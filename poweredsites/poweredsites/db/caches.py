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

from poweredsites.db.mongodb import MongodbModel
from poweredsites.db import conn

_collection = "caches"

class Cache(MongodbModel):
    def collection(self):
        return _collection

    def attributes(self):
        return ["key", "value", "expire", "condition"]

    def findby_key(self, key):
        return self.db.find_one({"key":key})


class Page(Cache):
    def name(self):
        return "caches_page"

    def attributes(self):
        return ["key", "status", "headers", "chunk", "expire", "condition"]


def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("key", unique=True)

clearup = setup

