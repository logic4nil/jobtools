# -*- coding: utf-8 -*-

import gevent
from gevent import monkey
monkey.patch_all()

import subprocess
import tempfile
from const import Status

class BaseShellExec(object):
    def __init__(self, cmd, env={}):
        self.cmd = cmd
        self.env = env

        self._instance = subprocess.Popen(["/bin/bash", "-c", self.cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=self.env)

    @property
    def pid(self):
        return self._instance.pid

    @property
    def returncode(self):
        self._instance.wait()
        return self._instance.returncode

    @property
    def output(self):
        self._instance.wait()
        _output, _err = self._instance.communicate()
        return _output.decode()

    def kill(self):
        self._instance.kill()

class ShellExecTool(object):
    def __init__(self):
        pass

    @classmethod
    def execute(cls, cmd, env={}) :
        tmpfile = tempfile.NamedTemporaryFile(suffix=".sh", delete=True)
        result = None
        with open(tmpfile.name, "w") as tmp:
            tmp.write("#!/bin/bash\n")
            for k, v in env.items(): 
                tmp.write("%s=%s\n" % (k, v))
            tmp.flush()

            s = BaseShellExec("source %s; %s" % (tmpfile.name, cmd))
            
            if s.returncode != 0:
                raise ExpressionError("ShellExpress:'%s' Error" % cmd)
            else:
                result = s.output

        return result

def exec_shell(cmd, env={}):
    s = BaseShellExec(cmd, env)
    return s.output

if __name__ == '__main__':
    print(exec_shell("export b=$a; echo $b", {"a":"aaa"}));

