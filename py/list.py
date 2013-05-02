#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

## duplicates and list, tricks
## unique - remove duplicates
lst = [1,2,3,4,4,5,6,4,7]
res = list( set( lst ) )
print res
print "\n"



## duplicates - find equal elements
import collections
res = collections.Counter(lst)
print res
print "\n"
## prints Counter({4: 2, 1: 1, 2: 1, 3: 1, 5: 1, 6: 1, 7: 1})



## print list, starting from last element
for item in reversed(lst):
    print item



## select all greater than 3
res = [elem for elem in lst if lst[elem] > 3]
print res
print "\n"


## get list, each element added by 100
res = [elem for elem in map(lambda x: x + 100, lst ) ]
print res
print "\n"


## print list columnwise / formats, etc
print '%s' % '\n' .join( map( str, lst ))


## set pointer to a list
arr = lst
## removing, in arr or in lst is equal!


## deep copy a list
arr = [r for r in lst]
# or - but this MAY NOT be the same, to make deep copy sure use the FIRST expression
arr = lst[:]



# To sort the list in place..., when var is "count"
ut.sort(key=lambda x: x.count, reverse=True)



# To return a new list, use the sorted() built-in function..., when var is "count"
newlist = sorted(ut, key=lambda x: x.count, reverse=True)



# find first occurence of an element with specified conditions in a list
lst = ["aaa", "bbb", "ccc"]

## find first occurence of elem x, that is not elem y
res = next((i for i, y in enumerate(lst) if y != x), -1)

## find first occurence of element with item "bbb"
res = next((i for i in lst if i == "bbb"), -1)



## dictionary
dicto {'a':[1], 'b':[2,4], 'c':3}

## append elemnts
dicto.append({'f':"bleble"})

## copy dict
import copy
dictocopy = copy.deepcopy( dicto )



## find index of element in list
lst = ["foo", "bar", "baz"]
idx = lst.index('bar')



## remove empty lines in a multiline string "text"
text = os.linesep.join([s for s in text.splitlines() if s])


