#!/usr/bin/python3

## note: an already existing output file will be overwritten!
def file_copy_replace(infile, outfile, oldtext, newtext):
    fin = open(infile, 'rt')
    fout = open(outfile, 'wt')
    for line in fin:
        fout.write(line.replace(oldtext, newtext))
    fin.close()
    fout.close()

infile = 'test.txt'
outfile = 'out.txt'

## if oldtext and newtext are '', the file is just copied over
oldtext = 'jack'
newtext = 'maria'

file_copy_replace(infile, outfile, oldtext, newtext)
print('READY.')
