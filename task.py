# -*- coding: utf-8 -*-
import gevent
from gevent.queue import JoinableQueue
from gevent import monkey
monkey.patch_all()

import sys
import re
import logging

from shell import BaseShellExec

class Task(object):
    def __init__(self, taskdesc, logfile=None, prefn = None, callback=None):
        self.logger = logging.getLogger("task")

        self.taskdesc = taskdesc
        self.env = {}

        self.logfile = logfile
        if self.logfile:
            self.logfd = open(logfile, "w")
        else:
            self.logfd = sys.stdout

        self.exports = {}

        self.prefn = prefn
        self.callback = callback

    @property
    def name(self):
        return self.taskdesc.name

    def run(self):
        if self.prefn:
            self.prefn(self)

        cmd = self.taskdesc.generate_cmd()
        exe = BaseShellExec(cmd, self.env)

        self.output = exe.output.strip()
        self.logger.debug("Task:%s [output: %s]" % (self.taskdesc.name, self.output))

        print("t" * 100)

        self.export_env()

        if self.callback:
            self.callback(self)

    def export_env(self):
        '''
        Catch Export Env Use The output
        '''
        reg = re.compile(r'##(\w+?)=(.*?)##')
        for line in self.output.split("\n"):
            if line.startswith("##"):
                m = reg.match(line)
                if m:
                    _data = m.groups()
                    if len(_data) == 2:
                        self.exports[_data[0]] = _data[1]

                        self.logger.info("Task: %s [export %s:%s]" % (self.taskdesc.name, _data[0], _data[1]))

class TaskPoolExecutor(object):
    def __init__(self, parallels=10):
        self.parallels = parallels

        self._q = JoinableQueue()
        self.threads = [gevent.spawn(self.worker) for _ in range(parallels)]

        self.logger = logging.getLogger("task.executor")

    def worker(self):
        while True:
            task= self._q.get()
            try:
                print("t" * 10)
                self.logger.info("Start Task: %s", task.name)
                task.run()
                self.logger.info("End Task: %s", task.name)
            except Exception as e:
                logger.warn(e)
            finally:
                self._q.task_done()

    def start(self):
        gevent.joinall(self.threads)

    def submit(self, task):
        self._q.put(task)

