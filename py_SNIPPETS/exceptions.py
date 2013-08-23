#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01


## set up exception, raise it and catch it
try:
    raise Exception( "some text" )
except Exception,e :
    print "Caught: ", e

## ...in case print traceback
except:
    import traceback
    traceback.print_exc()


## customized exception
##
## RESOURCE:
## http://docs.python.org/2/tutorial/errors.html
class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    

try:
    raise MyError(2*2)
except MyError as e:
    print 'My exception occurred, value:', e.value


