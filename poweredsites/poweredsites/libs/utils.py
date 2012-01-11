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

import os
import logging
import shlex
import subprocess
import tornado
from tornado.options import define, options
from tornado.web import URLSpec

class _NoDefault:
    """No default value rather than confused None"""
    def __repr__(self):
        return '(No Default)'
NoDefault = _NoDefault()

def find_modules(modules_dir):
    try:
        return [f[:-3] for f in os.listdir(modules_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []

def parse_config_file(path):
    """Rewrite tornado default parse_config_file.
    
    Parses and loads the Python config file at the given path.
    
    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}
    execfile(path, config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])

def url(pattern, handler_class, prefix="", **kwargs):
    """Make it easy to write url for a suite of handlers"""
    if not prefix.startswith("^"):
        prefix = "^" + prefix
    if prefix.endswith("$"):
        prefix = prefix[:-1]

    pattern = prefix + pattern
    pattern = pattern.replace("//", "/")
    name = kwargs.pop("name", None)
    if name is not None:
        return URLSpec(pattern, handler_class, kwargs, name)  # as URLSpec's parameter
    else:
        return pattern, handler_class, kwargs


################################################################################
#
# AsyncProcessMixin is borrowed from Philip Plante
# http://gist.github.com/489093
#
# Copyright (c) 2010, Philip Plante of EndlessPaths.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
class AsyncProcessMixin(object):
    def call_subprocess(self, command, callback=None):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.pipe = p = subprocess.Popen(shlex.split(command), \
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT, close_fds=True)
        self.ioloop.add_handler(p.stdout.fileno(), \
                self.async_callback(self.on_subprocess_result, \
                callback), self.ioloop.READ)

    def on_subprocess_result(self, callback, fd, result):
        try:
            if callback:
                callback(self.pipe.stdout)
        except Exception, e:
            logging.error(e)
        finally:
            self.ioloop.remove_handler(fd)

