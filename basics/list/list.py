#!/usr/bin/python3
print('list - operations and tricks')
print('\n\n')
i = 0

i+=1; print('%d. unique - remove duplicates'%i)
listi = [1,4,1,5,6,7,3,3,5,2,8,2]
print('orig:',listi)
res = list( set( listi ) )
print('res:',res)
print('')



i+=1; print('%d. duplicates - find equal elements'%i)
import collections
print('orig:',listi)
res = collections.Counter(listi)
print('res:',res)
print('')
## prints Counter({4: 2, 1: 1, 2: 1, 3: 1, 5: 1, 6: 1, 7: 1})



i+=1; print('%d. reverse - starting from last element'%i)
print('orig:',listi)
for item in reversed(listi): print(item)
print('')



i+=1; print('%d. filter - select all greater than 3'%i)
print('orig:',listi)
res = [elem for elem in listi if listi[elem] > 3]
print('res:',res)
print('')



i+=1; print('%d. each - get list, each element added by 100'%i)
print('orig:',listi)
res = [elem for elem in map(lambda x: x + 100, listi ) ]
print('res:',res)
print('')



i+=1; print('%d. all indexes of a specific element in a list - here print all indexes of elment "5"'%i)
arr = [1,2,3,4,5,1,5,2,3,5]
print('arr:', arr)
brr = [i for i, j in enumerate(arr) if j == 5]
print('brr:', brr)
print('number of elements x in list, e.g. "5"')
print('arr.count(5):', arr.count(5))
print('')



i+=1; print('%d. print list columnwise / formats, etc'%i)
print('orig:',listi)
print('%s' % '\n'.join( map( str, listi )))
print('')



i+=1; print('%d. set pointer to a list: arr = lst'%i)
print('orig:',listi)
arr = listi
print('removing, in arr or in lst is the SAME!')
print('')



i+=1; print('%d. deep copy a list'%i)
arr = [r for r in listi]
print('arr:', arr)
print('...or - but this MAY NOT be the same, to make deep copy sure use the FIRST expression')
arr = listi[:]
print('arr:', arr)
print('')



i+=1; print('%d. to sort the list in place..., when var is "count"'%i)
ut = ['a', 'z', 'c', 'y', 'b', 'x' ]
print('ut:', ut)
ut.sort() ## using sort()
print('ut (sort):', ut)
print('to return a new list, use the sorted() built-in function..., when var is "count"')
ut = sorted(ut, reverse = True) ## using sorted()
print('ut (reverse):', ut)
print('')



i+=1; print('%d. find first occurence of elem x, that is not elem y'%i)
print('orig:',listi)
x = 3
res = next((i for i, y in enumerate(listi) if y != x), -1)
print('first occurrence of %s: %s' % (x, res))
print('')



i+=1; print('%d. find first occurence of element with item "bbb"'%i)
print('orig:',listi)
res = next((i for i in listi if i == "bbb"), -1)
print(res)
print('')



i+=1; print('%d. find index of element in list'%i)
print('orig:',listi)
#listi = ["foo", "bar", "baz"]
#idx = listi.index('bar')
idx = listi.index(3)
print('idx', idx)
print('')



i+=1; print('%d. remove empty lines in a multiline string "text"'%i)
import os
text = "foo\nbar\nber baz"
text = os.linesep.join([s for s in text.splitlines() if s])
print(text)
print('')


print('READY.')
