#!/usr/bin/python3

import subprocess
import shlex

command = shlex.split('hostname -I')
ips = []

ips_raw = subprocess.run(command, capture_output=True, encoding='utf-8')
ips_raw = ips_raw.stdout.strip('\n')
ips += ips_raw.split(' ')
ips = list(filter(None, ips)) # chomp

print(ips)
print('len =', len(ips))


print('READY.')
