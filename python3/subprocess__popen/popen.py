#!/usr/bin/python3
##
## os.popen() is deprecated since python 2.6
##
##
## python2:
##
## Method   | Arguments
## ---------+-------------------------
## popen()  | stdout
## popen2() | stdin, stdout
## popen3() | stdin, stdout, stderr
## popen4() | stdin, stdout and stderr
##
##
##
## converting:
##
## in python2                                                       | replaced by / python3
## -----------------------------------------------------------------+----------------------------------------------------------------------
## pipe = os.popen('cmd', 'r', bufsize)                             | pipe = Popen('cmd', shell=True, bufsize=bufsize, stdout=PIPE).stdout
## pipe = os.popen('cmd', 'w', bufsize)                             | pipe = Popen('cmd', shell=True, bufsize=bufsize, stdin=PIPE).stdin
##                                                                  |
## (child_stdin, child_stdout) = os.popen2('cmd', mode, bufsize)    | p = Popen('cmd', shell=True, bufsize=bufsize, stdin=PIPE, stdout=PIPE, close_fds=True)
##                                                                  | (child_stdin, child_stdout) = (p.stdin, p.stdout)
##                                                                  |
## (child_stdin,                                                    | p = Popen('cmd', shell=True, bufsize=bufsize,
## child_stdout,                                                    |         stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
## child_stderr) = os.popen3('cmd', mode, bufsize)                  | (child_stdin, child_stdout, child_stderr) = (p.stdin, p.stdout, p.stderr)
##                                                                  |
## (child_stdin, child_stdout_and_stderr) =                         | p = Popen('cmd', shell=True, bufsize=bufsize,
##        os.popen4('cmd', mode, bufsize)                           |         stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
##                                                                  | (child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)
##
##
##
## NB: The recommended approach to invoking subprocesses is to use the run()
## function for all use cases it can handle. For more advanced use cases, the
## underlying Popen interface can be used directly.
##
## NB: Pexpect can be another alternative to subprocess!

import os
import subprocess


## python2: os.popen() - deprecated since python 2.6!!!
#cmd = 'git ls-remote --heads https://github.com/Rubusch/linux'
#repo_listing = [line.rstrip('\n').split('\t')[1] for line in os.popen( cmd )]

## NB: separate check for exit value needed, in all cases


## python3: subprocess
##
## get list output from command
try:
    cmd = 'git ls-remote --heads https://github.com/Rubusch/linux'
    #cmd = 'exit 1' ## uncomment to test exception

    ## subprocess.run() - offers timeout and exception mechanism
    repo_listing = subprocess.run(cmd, shell=True, encoding='utf-8', check=True, stdout=subprocess.PIPE).stdout.split('\n') ## is able to throw exception
    repo_listing = list(filter(None, repo_listing)) ## remove empty type
    repo_listing = [line.split('\t')[1] for line in repo_listing] ## splitting to final list

    print(repo_listing)
    print('')

except subprocess.CalledProcessError as e:
    ## python3 allows for exception handling
    print('XXX an error was caught XXX')
    print(e.output)

print("READY.\n")
