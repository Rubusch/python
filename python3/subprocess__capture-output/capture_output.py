#!/usr/bin/python3

import subprocess


## the following will fail when using '"', e.g. 'vagrant ssh client -c "hostname -I"'
import shlex

ips=[]
command = shlex.split('hostname -I')
ips_raw = subprocess.run(command, capture_output=True, encoding='utf-8')
ips_raw = ips_raw.stdout.strip('\n')
ips += ips_raw.split(' ')
ips = list(filter(None, ips)) # chomp

print('subprocess.run(), ips:', ips)
print('len =', len(ips), '(no empty elements contained)')
print('')


## the follwoing can handle '"', but 'shell=True' may be insecure
import re

ips = []
process = subprocess.Popen('hostname -I', shell=True, stdout=subprocess.PIPE)
for line in process.stdout: ips += re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(line))

print('subprocess.Popen(), ips:', ips)
print('len =', len(ips), '(no empty elements contained)')
print('')


print('READY.')
