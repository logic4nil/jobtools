# -*- coding: utf-8 -*-
from shell import exec_shell, ShellExecTool
from exceptions import ExpressionError

class Expression(object):
        pass

class ShellExpression(Expression):
    def __init__(self, value, env={}):
        self.env = env
        self.raw = value

    def value(self):
        # return exec_shell(self.raw, env=self.env)
        return ShellExecTool.execute(self.raw, env=self.env)

class ConstExpression(Expression):
    def __init__(self, value):
        self.raw = value

    def value(self):
        return self.raw

class ExpressionFactory(object):
    def __init__(self):
        pass

    @classmethod
    def make(cls, exp, env={}):
        if exp.startswith("@shell:"):
            return ShellExpression(exp[len("@shell:"):], env).value()
        elif exp.startswith("@const:"):
            return ConstExpression(exp[len("@const:"):]).value()
        else:
            return ConstExpression(exp).value()

if __name__ == "__main__":
    s = ExpressionFactory.make("@shell:echo $a", {"a":10})
    print(s)
    # print(s.value())
