#!/usr/bin/python3

## dictionary
dicto = {'a':[1], 'b':[2,4], 'c':3}

## append elemnts
dicto.append({'f':"bleble"})

## copy dict
import copy
dictocopy = copy.deepcopy( dicto )

print('READY.')
