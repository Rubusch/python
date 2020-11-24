#!/usr/bin/python3

fin=open('./test.txt')

# print file open mode
print('print file open mode:', fin)
print('\n')

# print one line
print('print single line:', fin.readline())
print('\n')

# print the further content
print('print further content:', fin.readlines())
print('\n')

fin.close()


# print nicer
fin=open('./test.txt')
for line in fin:
    print('print nicer:', line)
fin.close()
print('\n')

print("READY.\n")
