# -*- coding: utf-8 -*-
import os
import urllib.parse

import const
from exceptions import ProjectFileNotExistError

class PDLoader(object):
    def open(self, path):
        raise NotImplementedError("Class %s does not implement function open" % (self.__class__.__name__))

class HdfsFilePDLoader(PDLoader):
    def __init__(self):
        pass

    def open(self, path):
        pass

class LocalFilePDLoader(PDLoader):
    def __init__(self):
        pass

    def open(self, path):
        p = urllib.parse.urlparse(path)  

        loc = p.path
        if os.path.exists(loc):
            return open(loc, "r")

        for ext in list(const.Exts):
            loc = "%s.%s" % (loc, ext.name.lower())
            return open(loc, "r")

        raise ProjectFileNotExistError("The File %s Not Exists" % path)

localLoader = LocalFilePDLoader()
hdfsLoader = HdfsFilePDLoader()

FINDERS = {
    "file": localLoader,
    "hdfs": hdfsLoader
}
DEFAULTLOADER = localLoader

def get(path):
    loader = DEFAULTLOADER
    p = urllib.parse.urlparse(path)  
    if p.scheme in FINDERS:
        loader = FINDERS.get(p.schema)

    return loader

def load(path):
    loader = get(path)
    return loader.open(path)

