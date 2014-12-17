#!/usr/bin/env python

#
# Copyright (C) 2014 Simone Basso <bassosimone@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""" Integration tests for the deployed WAR """

import httplib
import json
import os.path
import unittest

SETTINGS = {
    'prefix': '/tmfcore',  # Assuming Tomcat
    'port': 8080,
    'topdir': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
}

def _dbpedia(concept):
    """ Map concept to its dbpedia URI """
    return "http://dbpedia.org/resource/" + concept

class TestNormalBehavior(unittest.TestCase):
    """ Test normal behavior of the deployed WAR """

    def test_classify_short(self):
        """ Test that /2.0/classify/short works as expected """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            "text": open(filepath, "r").read(),
            "lang": "us",
            "numTopics": 4
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertEqual(resp.status, 200)

        respdict = json.loads(resp.read())

        self.assertEqual(len(respdict), 4)
        self.assertEqual(respdict[0]["uri"], _dbpedia("ASCII"))
        self.assertEqual(respdict[1]["uri"], _dbpedia("Agricultural_science"))
        self.assertEqual(respdict[2]["uri"], _dbpedia("Apollo_11"))
        self.assertEqual(respdict[3]["uri"], _dbpedia("Android_(robot)"))

    def test_classify(self):
        """ Test that /2.0/classify works as expected """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "LICENSE"])
        bodydict = {
            "text": open(filepath, "r").read(),
            "lang": "us",
            "numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertEqual(resp.status, 200)

        respdict = json.loads(resp.read())

        self.assertEqual(len(respdict), 8)
        self.assertEqual(respdict[0]["uri"], _dbpedia("Aristotle"))
        self.assertEqual(respdict[1]["uri"], _dbpedia("Agricultural_science"))
        self.assertEqual(respdict[2]["uri"], _dbpedia("ASCII"))
        self.assertEqual(respdict[3]["uri"], _dbpedia(
            "American_National_Standards_Institute"))
        self.assertEqual(respdict[4]["uri"], _dbpedia("Agriculture"))
        self.assertEqual(respdict[5]["uri"], _dbpedia("Animalia_(book)"))
        self.assertEqual(respdict[6]["uri"], _dbpedia("Anarchism"))
        self.assertEqual(respdict[7]["uri"], _dbpedia("Alphabet"))

class TestClassifyShortRobustness(unittest.TestCase):
    """ Test that /classify/short is robust enough """

    def test_empty_body(self):
        """ Test that an empty body causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        body = ""

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_invalid_json(self):
        """ Test that an invalid JSON causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        body = "[1, 2, 3}"

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_empty_dict(self):
        """ Test that an empty dictionary causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_missing_num_topics(self):
        """ Test that numTopics must causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            "text": open(filepath, "r").read(),
            "lang": "us",
            #"numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_missing_lang(self):
        """ Test that lang must be present """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            "text": open(filepath, "r").read(),
            #"lang": "us",
            "numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_missing_text(self):
        """ Test that text must be present """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            #"text": open(filepath, "r").read(),
            "lang": "us",
            "numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

class TestClassifyRobustness(unittest.TestCase):
    """ Test that /classify is robust enough """

    def test_empty_body(self):
        """ Test that an empty body causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        body = ""

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_invalid_json(self):
        """ Test that an invalid JSON causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        body = "[1, 2, 3}"

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_empty_dict(self):
        """ Test that an empty dictionary causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_missing_num_topics(self):
        """ Test that numTopics must causes an error """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            "text": open(filepath, "r").read(),
            "lang": "us",
            #"numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_missing_lang(self):
        """ Test that lang must be present """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            "text": open(filepath, "r").read(),
            #"lang": "us",
            "numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

    def test_missing_text(self):
        """ Test that text must be present """

        url = SETTINGS['prefix'] + "/2.0/classify"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        #filepath = os.sep.join([SETTINGS['topdir'], "README.md"])
        bodydict = {
            #"text": open(filepath, "r").read(),
            "lang": "us",
            "numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

class TestClassifyShortWithLongInput(unittest.TestCase):
    """ Test that /classify/short with long input """

    def test_should_fail(self):
        """ Test that long input causes a /classify/short error """

        url = SETTINGS['prefix'] + "/2.0/classify/short"
        conn = httplib.HTTPConnection("127.0.0.1", SETTINGS['port'])
        filepath = os.sep.join([SETTINGS['topdir'], "LICENSE"])
        bodydict = {
            "text": open(filepath, "r").read(),
            "lang": "us",
            "numTopics": 8
        }
        body = json.dumps(bodydict)

        conn.request("POST", url, body, {
            "Content-Type": "application/json",
            "Content-Length": len(body),
            "Accept": "application/json",
            "Connection": "close"
        })

        resp = conn.getresponse()

        self.assertFalse(resp.status == 200)

def main():
    """ Main function """
    unittest.main()

if __name__ == "__main__":
    main()
