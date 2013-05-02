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
