#!/usr/bin/env python3

import argparse
import copy
import curses
import hashlib
import math
import os
import re
import signal
import time
from threading import Lock
from typing import Tuple, Dict

import colorama
from sh import bash
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

parser = argparse.ArgumentParser()
parser.add_argument('compose', type=str, default='__DEFAULT__', help='A job definition')
parser.add_argument('--jobs', type=str, default='+all', metavar='name', required=False, nargs='+',
                    help='What to run. User +job, +tag to include a jobs by tag or a job.'
                         'Use _job, _tag to exclude jobs.'
                         'Use special keyword all to match all jobs')
parser.add_argument("--dry", action='store_true')

pgids = []
stop = False

def signal_handler(sig, frame):
    print("CTRL+C Detected, please wait for all processes to exit...")

    global stop
    stop = True

    for pgid in pgids:
        try:
            os.killpg(pgid, 15)
        except Exception:
            pass

signal.signal(signal.SIGINT, signal_handler)


class StdoutPrinter:

    def __init__(self, stdscr):
        self.stdsrc = stdscr
        colors = [value for name, value in list(vars(colorama.Fore).items())]
        colors.remove(colorama.Fore.RESET)
        colors.remove(colorama.Fore.BLACK)
        colors.remove(colorama.Fore.LIGHTBLACK_EX)
        colors.remove(colorama.Fore.LIGHTWHITE_EX)
        colors.remove(colorama.Fore.WHITE)

        colorama.init()
        self.colors = colors

        self.logs = {}
        self.assigned_colors = {}

        self.mutex = Lock()

        if "TERM" not in os.environ:
            os.environ["TERM"] = "xterm-256color"

        self.windows = {}

    def prepare(self, compose):

        stdscr = self.stdsrc
        rows, cols = stdscr.getmaxyx()

        rows_per_job = rows // len(compose['services'])
        rows_per_job *= 2

        cols_per_job = cols // 2

        serv_len = len(compose['services'])

        table_columns = 2
        table_rows = math.ceil(serv_len / 2)

        column = 0
        row = 0

        for i, job in enumerate(compose['services']):
            color = self.colors[compose['services'][job]['hash'] % len(self.colors)] if compose is not None else ''
            self.assigned_colors[job] = color
            self.colors.remove(color)

            self.logs[job] = []
            self.windows[job] = curses.newwin(rows_per_job, cols_per_job, row * rows_per_job, column * cols_per_job)
            self.windows[job].border(' ', ' ', '-', ' ', '+', '+', ' ', ' ')
            self.windows[job].addstr(0, 4, f"{job}")
            self.windows[job].refresh()

            column += 1

            if column >= table_columns:
                column = 0
                row += 1


    def process_output_paned(self, job, compose, line, err=False):
        self.mutex.acquire()

        if line.endswith('\n'):
            line = line[0:len(line) - 1]

        def escape_ansi(l):
            ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            return ansi_escape.sub('', l)

        line = escape_ansi(line)

        window = self.windows[job]
        rows, cols = window.getmaxyx()
        rows -= 1
        cols -= 2

        lines = [line[i:i + cols] for i in range(0, len(line), cols)]

        self.logs[job] += lines
        self.logs[job] = self.logs[job][-rows:]

        window.clear()
        self.windows[job].border(' ', ' ', '-', ' ', '+', '+', ' ', ' ')
        self.windows[job].addstr(0, 4, f"{job}")
        for i, line in enumerate(self.logs[job]):
            window.addstr(i + 1, 1, line)

        window.refresh()

        self.mutex.release()

    def process_output(self, job, compose, line, err=False):
        if line.endswith('\n'):
            line = line[0:len(line) - 1]

        if job not in self.assigned_colors:
            color = self.colors[compose['services'][job]['hash'] % len(self.colors)] if compose is not None else ''
            self.assigned_colors[job] = color
            self.colors.remove(color)
        else:
            color = self.assigned_colors[job]

        self.mutex.acquire()
        print(color + job + colorama.Fore.RESET, end=' ')
        print("| " + (colorama.Fore.RED if err else '') + line + colorama.Fore.RESET)
        self.mutex.release()


def run_service(compose, service_name, services, printer):
    definition = compose['services'][service_name]

    stdin = ";\n".join(compose['pre']) + ";\n"

    stdin += f"cd {definition['working_dir']};\n"
    stdin += definition["command"] + ";\n" if definition['command'] else ''
    stdin += ";\n".join(definition["commands"]) + ";\n" if definition['commands'] else ''

    stdin += ";\n".join(compose['post']) + ";\n"

    service = bash(_in=stdin,
                   _out=(lambda j: (lambda line: printer.process_output_paned(j, compose, line, False)))(service_name),
                   _err=(lambda j: (lambda line: printer.process_output_paned(j, compose, line, True)))(service_name),
                   _bg=True,
                   _new_session=False)

    global pgids
    pgids += [service.pgid]
    services += [service]
    return service.pgid


def healthcheck_ok(compose, service_name):

    if "healthcheck" not in compose["services"][service_name]:
        return True

    stdin = ";\n".join(compose['pre']) + ";\n"
    stdin += compose["services"][service_name]["healthcheck"] + ";\n"
    stdin += "echo -n $?;\n"

    code = [-1]

    def set_code(c):
        c = str(c).replace("\n", "")
        try:
            code[0] = int(c)
        except Exception:
            pass

    bash(_in=stdin, _out=lambda line: set_code(line))

    while code[0] == -1:
        time.sleep(0.5)

    return code[0] == 0

def run(stdscr, compose):
    printer = StdoutPrinter(stdscr)
    printer.prepare(compose)

    services = []
    started_at = {}
    k_pgids = {}

    for service_name in compose["services"]:
        pgid = run_service(compose, service_name, services, printer)
        started_at[service_name] = time.time()
        k_pgids[service_name] = pgid

    while not stop:

        for service_name in compose["services"]:
            if time.time() - started_at[service_name] > 60:
                if not healthcheck_ok(compose, service_name):
                    printer.process_output_paned(service_name, compose, "=== HEALTH CHECK FAILED ===", err = True)

                    try:
                        os.killpg(k_pgids[service_name], 9)
                    except Exception:
                        pass

                    time.sleep(1)
                    pgid = run_service(compose, service_name, services, printer)
                    started_at[service_name] = time.time()
                    k_pgids[service_name] = pgid

        stdscr.refresh()
        time.sleep(1)

    for service in services:
        service.wait()


def filter_jobs(compose, jobs) -> Tuple[bool, str, Dict]:
    filtered_compose = copy.deepcopy(compose)
    filtered_compose['services'] = {}

    for name in jobs:
        mode = 'remove' if name[0] == '-' or name[0] == '_' else 'append'

        if name[0] == '+' or name[0] == '-' or name[0] == '_':
            name = name[1:]

        if name in compose['services']:

            if mode == 'append':
                filtered_compose['services'][name] = compose['services'][name]
            elif mode == 'remove':
                filtered_compose['services'].pop(name, None)

        else:
            found = False

            for service_n in compose['services']:
                service = compose['services'][service_n]

                if name in service['tags']:
                    if mode == 'append':
                        filtered_compose['services'][service_n] = compose['services'][service_n]
                    elif mode == 'remove':
                        filtered_compose['services'].pop(service_n, None)

                    found = True

            if not found:
                return False, f"Failed to find job / tag {name}", {}

    return True, '', filtered_compose


def validate(compose) -> Tuple[bool, str]:

    compose['pre'] = compose['pre'] if 'pre' in compose else []
    compose['post'] = compose['post'] if 'post' in compose else []
    compose['visible'] = 0

    for job in compose['services']:
        definition = compose['services'][job]

        definition['command'] = definition['command'] if 'command' in definition else ''
        definition['commands'] = definition['commands'] if 'commands' in definition else []

        definition['working_dir'] = definition['working_dir'] if 'working_dir' in definition else '.'

        definition['hash'] = int(hashlib.sha1(job.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        definition['tags'] = definition['tags'] if 'tags' in definition else []
        definition['tags'] += ['all']

        definition['bg'] = definition['bg'] if 'bg' in definition else False

        if not definition['bg']:
            compose['visible'] += 1

    return True, ''


def print_jobs(compose):

    for service in compose['services']:
        definition = compose['services'][service]

        print(colorama.Style.BRIGHT, end='')
        print(f"== {service} ==")
        print(colorama.Style.RESET_ALL, end='')

        for command in compose['pre']:
            print(command)

        print(f"cd {definition['working_dir']}")

        if 'command' in definition and definition['command']:
            print(definition['command'])

        for command in definition['commands']:
            print(command)

        for command in compose['post']:
            print(command)

        print("\n")

def main(stdscr, args):
    with open(args.compose, 'r') as f:
        compose = load(f, Loader=Loader)

    ok, err = validate(compose)

    if not ok:
        print(f"Compose is not valid due to: {err}")
        return

    if type(args.jobs) is not list:
        args.jobs = [args.jobs]

    ok, err, compose = filter_jobs(compose, args.jobs)

    if not ok:
        print(f"Compose is not valid due to: {err}")
        return

    if args.dry:
        print_jobs(compose)
        return

    run(stdscr, compose)


def entrypoint():
    args = parser.parse_args()
    curses.wrapper(main, args)

if __name__ == '__main__':
    entrypoint()
