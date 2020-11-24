#!/usr/bin/python3

## convert dictionary string to dictionary using ast.literal_eval()
import ast

## initializing string, must have:
## ' - for the outer string and
## " - for the inner elements, to be dict keys
test_string = '{"Name2" : 2, "Name3": 3, "Name1": 1}'

## printing original string
print('before (string): ' + str(test_string))

## using ast.literal_eval() convert dictionary string to dictionary
res = ast.literal_eval(test_string)

# print result
print('after (dictionary): ' + str(res))


print("READY.\n")
