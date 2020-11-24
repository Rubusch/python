#!/usr/bin/python3

## convert dictionary string to dictionary using json.loads()
import json

## initializing string, must have:
## ' - for the outer string and
## " - for the inner elements, to be dict keys
test_string = '{"Name2" : 2, "Name3": 3, "Name1": 1}'

## printing original string
print('before (string): ' + str(test_string))

## using json.loads() convert dictionary string to dictionary
res = json.loads(test_string)

# print result
print('after (dictionary): ' + str(res))


print("READY.\n")
