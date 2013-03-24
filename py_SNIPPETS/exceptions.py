## 

## set up exception, raise it and catch it
try:
    raise Exception( "some text" )
except Exception,e :
    print "Caught: ", e

## ...in case print traceback
except:
    import traceback
    traceback.print_exc()
