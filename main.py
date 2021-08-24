#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging

logging.basicConfig(
    stream = sys.stdout,
    level = logging.DEBUG,
    format = '%(asctime)s.%(msecs)d %(levelname)s %(pathname)s [line:%(lineno)d] - fun:%(funcName)s - %(message)s',
    datefmt = '%Y/%m/%d %H:%M:%S'
)


import atexit

from descriptor import ProjectDescriptor
from job import JobContext

@atexit.register
def gooldbye():
    print("You are now leaving jobtools")

def main():
    desc = ProjectDescriptor("./demo.json")
    jobcontext = JobContext(desc)
    job = jobcontext.job()
    for t in job.runnable_tasks():
        job.run_task(t)


if __name__ == '__main__':
    main()
