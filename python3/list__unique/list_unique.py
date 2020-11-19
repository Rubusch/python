#!/usr/bin/python3

def out( mesg, item_list ):
    print(mesg)
    for item in item_list: print(item)
    print('')


arr = [ 'a', 'b', 'c' ]
out( '1. raw', arr )

arr.append( 'a' )
out( '2. append a', arr )

arr = set( arr )
out( '3. unique', arr )


print('READY.')

