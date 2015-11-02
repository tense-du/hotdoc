import os
import cPickle as pickle
from datetime import datetime
from hotdoc.core.alchemy_integration import MutableObject

import traceback


class Link (MutableObject):
    def __init__(self, ref, title, id_):
        self._title = title
        self.ref = ref
        self.id_ = id_
        MutableObject.__init__(self)

    def get_link (self):
        return self.ref

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

class LinkResolver(object):
    def __init__(self, doc_tool):
        self.__links = {}
        self.doc_tool = doc_tool

    def get_named_link (self, name):
        if name in self.__links:
            return self.__links[name]

        sym = self.doc_tool.get_symbol(name)
        if sym:
            self.__links[name] = sym.link
            return sym.link

        self.__links[name] = None
        return None

    def add_link (self, link):
        if not link.id_ in self.__links:
            self.__links[link.id_] = link

    def upsert_link (self, link, overwrite_ref=False):
        elink = self.__links.get (link.id_)
        if elink:
            if elink.ref is None or overwrite_ref and link.ref:
                elink.ref = link.ref
            if link.title is not None:
                elink.title = link.title
            return elink
        self.add_link (link)
        return link

    def dump(self):
        pickle.dump(self.__links, open('hd_links.p', 'wb'))

    def load(self):
        self.__links = pickle.load(open('hd_links.p', 'rb'))
