#!/usr/bin/python3
import shutil


#### inplace replace
shutil.copy('test.txt.template', 'test.txt')

fio = open('test.txt', 'rt')
content = fio.read()
content = content.replace('jack', 'maria')
fio.close()

fio = open('test.txt', 'wt')
fio.write(content)
fio.close()

print('READY.')
