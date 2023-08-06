# -*- coding: utf-8 -*-

#Copyright (c) 2019 André Santos
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import os
from setuptools import setup, find_packages

extra_files = ["haros_plugin_pyflwor/plugin.yaml"]

setup(
    name = "haros_plugin_pyflwor",
    version = "0.2.1",
    author = "André Santos",
    author_email = "andre.f.santos@inesctec.pt",
    description = "HAROS plugin to query Configurations with Pyflwor.",
    license = "MIT",
    keywords = "ros query architecture model computation-graph",
    url = "https://github.com/git-afsantos/haros-plugin-pyflwor",
    packages = find_packages(),
    package_data = {"haros_plugin_pyflwor": extra_files},
    install_requires = ["pyflwor_ext>=1.2"],
    zip_safe = True
)
