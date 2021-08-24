# -*- coding: utf-8 -*-

from const import Status
from expression import ExpressionFactory
from task import Task, TaskPoolExecutor

class JobContext(object):
    def __init__(self, pdesc):
        self.pb = pdesc
        self.envs = {}
        self.task_status = {}

    def setenv(self, k, v):
        self.envs[k] = v

    def runnable_tasks(self):
        tasks = set()
        for k, v in self.dag.items():
            if len(v) == 0:
                tasks.add(k)
        return tasks

    def job(self):
        return Job(self)

    def taskpool(self):
        return TaskPoolExecutor(max(self.pb.parallels, 1))

class Job(object):
    def __init__(self, context):
        self.context = context

        self.executor = context.taskpool()

        self._init_envs()
        self._build_dag()
    
    def _init_envs(self):
        '''
        初始化环境变量
        '''
        pb = self.context.pb
        envs = {}
        for p in pb.properties:
            self.context.setenv(p.name, p.value)
        for env in pb.envs:
            self.context.setenv(env.name, ExpressionFactory.make(env.value))

    def _build_dag(self):
        '''
        构建DAG
        '''
        pb = self.context.pb
        dag = {}

        for t in pb.tasks:
            dag[t.name] = t.depends

        self.context.dag = dag

    def _init_logger(self):
        self.logger = None

    def _init_persisit(self):
        pass

    def runnable_tasks(self):
        return self.context.runnable_tasks()

    def run_task(self, taskname, recursive=False):
        pb = self.context.pb
        taskdesc = pb.get_task_by_name(taskname)
        if not taskdesc is None:
            task = Task(taskdesc)
            self.executor.submit(task)

        self.executor.start()

    def run_all(self):
        pass


