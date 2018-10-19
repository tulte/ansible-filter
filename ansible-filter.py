#!/usr/bin/python

import subprocess
import sys
import os
import os.path

COLOR_YELLOW = 33
COLOR_RED = 31

CONFIG_FILE = 'ansible-filter.ignore'
FILTER_COL_TASK = 0
FILTER_COL_LINE = 1

command = 'ansible-playbook ' + ' '.join(sys.argv[1:])
task = None
recap = False


def write_colored_text(text, color_number):
    sys.stdout.write('\033[0;{}m{}\033[0;0m'.format(color_number, text))


def task_ignore_list():
    config_file = os.getcwd() + '/' + CONFIG_FILE
    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            return [(entry.split(';')) for entry in f.read().splitlines()]
    return []


def ignore_changed(ignore_entries, task, line):
    for ignore_entry in ignore_entries:
        if ignore_entry[FILTER_COL_TASK] in task and ignore_entry[FILTER_COL_LINE] in line:
            return True
    return False


ignore_entries = task_ignore_list()
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
mode = None
for line in iter(process.stdout.readline, ''):
    if line.startswith('TASK'):
        task = line
        mode = None
    elif line.startswith('PLAY RECAP') or recap:
        sys.stdout.write(line)
        mode = 'RECAP'
    elif line.startswith('fatal:'):
        write_colored_text(line, COLOR_RED)
        mode = 'FATAL'
    elif line.startswith('changed:'):
        if ignore_changed(ignore_entries, task, line) is False:
            sys.stdout.write(task)
            write_colored_text(line, COLOR_YELLOW)
            mode = 'CHANGED'
    elif mode == 'CHANGED':
        write_colored_text(line, COLOR_YELLOW)
    elif mode == 'RECAP':
        sys.stdout.write(line)
