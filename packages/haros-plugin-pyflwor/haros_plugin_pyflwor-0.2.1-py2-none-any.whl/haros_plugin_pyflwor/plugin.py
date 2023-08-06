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


###############################################################################
# Imports
###############################################################################

from builtins import object
import errno
import logging
import os

from haros.metamodel import Resource, RosPrimitive

from .pyflwor_monkey_patch import make_parser


################################################################################
# Plugin Entry Point
################################################################################

log = logging.getLogger(__name__)

def configuration_analysis(iface, config):
    query_data = config.user_attributes.get("haros_plugin_pyflwor", ())
    if query_data:
        pyflwor = _setup()
        for query_datum in query_data:
            name = query_datum["name"]
            details = query_datum.get("details", None)
            query = query_datum["query"]
            matches = pyflwor.execute(query, config, name=name)
            _report(iface, matches, name=name, details=details)


################################################################################
# Query Engine
################################################################################

class QueryEngine(object):
    QUERY_CONTEXT = {
        "True": True,
        "False": False,
        "None": None,
        "abs": abs,
        "bool": bool,
        "cmp": cmp,
        "divmod": divmod,
        "float": float,
        "int": int,
        "isinstance": isinstance,
        "len": len,
        "long": int,
        "max": max,
        "min": min,
        "pow": pow,
        "sum": sum,
        "round": round
    }

    def __init__(self, pyflwor):
        self.pyflwor = pyflwor
        self.data = dict(self.QUERY_CONTEXT)
        self.data["is_rosglobal"] = QueryEngine.is_rosglobal

    def execute(self, query, config, name=None):
        self.data["config"] = config
        self.data["nodes"] = config.nodes
        self.data["topics"] = config.topics
        self.data["services"] = config.services
        self.data["parameters"] = config.parameters
        location = config.location
        try:
            return self.pyflwor(query, self.data)
        except SyntaxError as e:
            if name:
                log.error("SyntaxError on query (%s): %s", name, e)
            else:
                log.error("SyntaxError on unnamed query: %s", e)
        return ()

    @staticmethod
    def is_rosglobal(name):
        return name and name.startswith("/")


################################################################################
# Helper Functions
################################################################################

def _setup():
    # create temp dir for pyflwor lexer files
    pyflwor_dir = os.path.join(os.getcwd(), "pyflwor")
    try:
        os.mkdir(pyflwor_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    pyflwor = make_parser(pyflwor_dir)
    query_engine = QueryEngine(pyflwor)
    return query_engine

RUNTIME_ENTITY = (Resource, RosPrimitive)

def _report(iface, matches, name="<unnamed>", details=None):
    # `matches` can be of types:
    # - pyflwor.OrderedSet.OrderedSet<object> for Path queries
    # - tuple<object> for FLWR queries single return
    # - tuple<tuple<object>> for FLWR queries multi return
    # - tuple<dict<str, object>> for FLWR queries named return
    # NOTE: sometimes 'object' can be a tuple or dict...
    n = 0
    for match in matches:
        log.debug("Query <%s> found: %s", name, match)
        value = None
        runtime_entities = []
        if isinstance(match, tuple):
            # assume tuple<tuple<object>> for FLWR queries multi return
            log.debug("Query match is a tuple")
            if len(match) == 1 and isinstance(match[0], tuple):
                match = match[0]
            for item in match:
                if isinstance(item, RUNTIME_ENTITY):
                    n += 1
                    runtime_entities.append(item)
                    log.debug("Query matched a runtime entity: %s", item)
        elif isinstance(match, dict):
            # assume tuple<dict<str, object>> for FLWR queries named return
            log.debug("Query match is a dict")
            for key, item in match.items():
                if isinstance(item, RUNTIME_ENTITY):
                    n += 1
                    runtime_entities.append(item)
                    log.debug("Query matched a runtime entity: %s", item)
        elif isinstance(match, RUNTIME_ENTITY):
            log.debug("Query match is a runtime entity: %s", match)
            n = 1
            runtime_entities.append(match)
        if not n:
            # literals and other return values
            log.debug("Query match is another type of value: %s", match)
            n = 1
            value = match
        if details:
            msg = details.format(entities=runtime_entities, value=value, n=n)
        else:
            msg = "Query {} found {} matches:\n{}".format(
                name, n, runtime_entities)
        log.info("Query <%s> found %d matches.", name, n)
        iface.report_runtime_violation("query", msg, resources=runtime_entities)
