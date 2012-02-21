#! /usr/bin/env python
import biplist
import json

class MetaParser(type):
    registry = {}
    def __new__(cls, name, bases, dict):
        new_cls = super(MetaParser, cls).__new__(cls, name, bases, dict)
        if 'format' in dict:
            cls.registry[dict['format']] = new_cls
        return new_cls

    @classmethod
    def get(cls, format):
        return cls.registry.get(format)

class JsonParser(object):
    __metaclass__ = MetaParser
    format = 'json'
    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)

class PlistParser(object):
    __metaclass__ = MetaParser
    format = 'plist'
    def encode(self, data):
        return biplist.writePlistToString(data)

    def decode(self, data):
        return biplist.readPlistFromString(data)
