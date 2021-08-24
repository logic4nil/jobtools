# -*- coding: utf-8 -*-
import os
import json

import loader
import const
from exceptions import ProjectFileNotExistError, ProjectConfigError

class Descriptor(object):
    pass

class ProjectDescriptor(Descriptor):
    def __init__(self, filepath):
        self.filepath = filepath
        self._load()

    def _load(self):
        try:
            fd = loader.load(self.filepath)
            self._raw = json.loads("".join(fd.readlines()))
            self._parse()
        except ProjectFileNotExistError as e:
            # TODO log
            print(e)

    def _parse(self):
        self.name = self._raw.get("name", None) or self.filepath
        self.extends = set()
        self.properties = set()
        self.envs = set()
        self.tasks = set()
        self.logger = None
        self.persistence = None

        self.parallels = self._raw.get("parallels", 10)

        try:
            self._parse_properties()
            self._parse_envs()
            self._parse_task()
            self._parse_logger()
            self._parse_persistence()
        except ProjectConfigError as e:
            # TODO LOG
            print("%s: %s" % (self.filepath, e))
            import traceback
            traceback.print_exc()
            exit(1)

        self.logger = self._raw.get("logger", None)
        self.persistence = self._raw.get("persistence", None)

        self._parse_extends()

        # TODO Check depends

    def _parse_extends(self):
        _raws = self._raw.get("extends", [])

        for _r in _raws:
            _extend_filepath = os.path.join(os.getcwd(), _r)
            _p = ProjectDescriptor(_extend_filepath)
            self.extends.add(_p)
            self.merge(_p)

    def _parse_properties(self):
        for k, v in self._raw.get("properties", {}).items():
            self.properties.add(PropertyDescriptor(k, v))

    def _parse_envs(self):
        _raws = self._raw.get("envs", [])
        for _r in _raws:
            self.envs.add(EnvDescriptor(_r))

    def _parse_task(self):
        _raws = self._raw.get("tasks", [])
        for _r in _raws:
            self.tasks.add(TaskDescriptor(_r))

    def _parse_logger(self):
        pass

    def _parse_persistence(self):
        pass

    def merge(self, other):
        if not isinstance(other, self.__class__):
            raise TypeNotMatchError("Merge Type Not Match")

        self.properties.update(other.properties)

        self.envs = self.envs | other.envs
        self.tasks = self.tasks | other.tasks

    def check_depends(self):
        # TODO
        pass

    def get_task_by_name(self, taskname):
        for t in self.tasks:
            if t.name == taskname:
                return t
        return None

    def __eq__(self, that):
        if not isinstance(that, self.__class__):
            return False
        return that.name == self.name and self.filepath == that.filepath

    def __hash__(self):
        return hash("%s_%s" % (self.name, self.filepath))

    def __str__(self):
        return '''
name: %s
extends: %s
properties: %s
envs: %s
tasks: %s
''' % (self.name, ",".join([x.name for x in self.extends]), ",".join(map(str, self.properties)), ",".join(map(str, self.envs)), ",".join(map(str, self.tasks)))
    

class PropertyDescriptor(Descriptor):
    def __init__(self, k, v):
        self.name = k
        self.value = v

    def __eq__(self, that):
        if not isinstance(that, self.__class__):
            return False
        return self.name == that.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "%s[%s]" % (self.name, self.value)

class EnvDescriptor(Descriptor):
    def __init__(self, data={}):
        self._raw = data
        self.name = self._raw.get("name", None)
        self.scope = const.EnvScope.from_str(self._raw.get("scope", "private"))
        self.value = self._raw.get("value", "")

    def __str__(self):
        return "%s[%s]" % (self.name, self.scope)

    def __eq__(self, that):
        if not isinstance(that, self.__class__):
            return False
        return self.name == that.name

    def __hash__(self):
        return hash(self.name)

class TaskDescriptor(Descriptor):
    def __init__(self, data={}):
        self._raw = data
        self.name = self._raw.get("name", None)
        if not self.name:
            raise ProjectConfigError("The config tasks.[].name is necessary")
        self.cmd = self._raw.get("cmd", None)
        self.retry = int(self._raw.get("retry", 0))
        self.exports = self._raw.get("exports", [])
        self.depends = self._raw.get("depends", [])

    def generate_cmd(self):
        cmd = self.cmd
        if len(self.exports) >=0:
            for e in self.exports:
                cmd = "%s; echo \"##%s=$%s##\"" % (cmd, e, e)
        return cmd

    def __eq__(self, that):
        if not isinstance(that, self.__class__):
            return False

        return self.name == that.name

    def __str__(self):
        return "%s[depends:%s, retry:%d]" % (self.name, ",".join(self.depends), self.retry)

    def __hash__(self):
        return hash(self.name)

class LogDescriptor(Descriptor):
    def __init__(self, data):
        self._raw = data

