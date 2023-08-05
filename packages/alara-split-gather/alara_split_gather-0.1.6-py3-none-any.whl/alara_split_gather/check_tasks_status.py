#!/usr/bin/env python3
import os
import argparse
import re
from alara_split_gather.utils import get_num_tasks

def check_status(sep='_', prefix='phtn_src'):
    # generate filenams for checking
    files = []
    sizes = []
    running = []
    finished = []
    # get the folders start with task*
    num_tasks = get_num_tasks()
#    files = os.listdir(os.path.abspath("."))
#    task_pattern = re.compile("^task*")
#    num_tasks = 0
#    for f in files:
#        if re.match(task_pattern, f):
#            num_tasks += 1
    print(f"{num_tasks} sub-task folders found")
    for i in range(num_tasks):
        filename = os.path.join(".", f"task{i}", f"{prefix}{sep}{i}")
        files.append(filename)
        size = os.path.getsize(filename)
        sizes.append(size)
        # count running/finshed status 
        if size > 5:
            finished.append(i)
        else:
            running.append(i)

    # print the summary
    # finished tasks
    fin_str = f"{len(finished)} sub-tasks are finished, they are:\n     "
    count = 0
    for i in finished:
        count += 1
        fin_str = f"{fin_str} {i}"
        if count>0  and count%10 == 0:
            fin_str = f"{fin_str}\n     "
    print(fin_str)
    # running tasks
    run_str = f"{len(running)} sub-tasks are running, they are:\n     "
    count = 0
    for i in running:
        count += 1
        run_str = f"{run_str} {i}"
        if count>0 and count%10 == 0:
            run_str = f"{run_str}\n     "
    print(run_str)

   
def alara_tasks_status():
    check_tasks_status_help = ('This script check the status of alara tasks\n')
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--separator", required=False, help=" '_' or '-'")
    parser.add_argument("-p", "--prefix", required=False, help="prefix of phtn_src")
    args = vars(parser.parse_args())

    # prefix
    prefix = "phtn_src"
    if args['prefix'] is not None:
        prefix = args['prefix']

   # separator
    sep = '_'
    if args['separator'] is not None:
        if args['separator'] not in ['_', '-']:
            raise ValueError(f"separator {args['separator']} not supported!")
        sep = args['separator']

    check_status(sep=sep, prefix=prefix)

if __name__ == '__main__':
    alara_tasks_status()
