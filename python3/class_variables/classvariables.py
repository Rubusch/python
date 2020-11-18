#!/usr/bin/python3
##
## demonstrates the scope of a variables among classes

class Parent:
    ## visible in derrived class
    var_static = "static parent"

    def __init__( self ):
        ## not visible in derrived
        self.var_dynamic = "dynamic parent"



class Child( Parent ):
    var_static_derrived = "static child"
    def __init__( self ):
        self.var_dynamic_derrived = "dynamic child"

    def changeVals( self ):
        self.var_static = "aniki"
        self.var_dynamic = "bobo"
        self.var_static_derrived = "passarinho"
        self.var_dynamic_derrived = "toto"

    def printAll( self ):
        print("static parent  - '%s'" % self.var_static)
        ## not visible here, results in error
        #print("dynamic parent - '%s'" % self.var_dynamic)
        print("dynamic parent - 'N/A'")
        print("static child  - '%s'" % self.var_static_derrived)
        print("dynamic child - '%s'" % self.var_dynamic_derrived)


## start

## instances
inst_A = Child()
inst_B = Child()
inst_C = Child()

print("inst_A.printAll()")
inst_A.printAll()

print("inst_B.changeVals()")
inst_B.changeVals()

print("inst_C.printAll()")
inst_C.printAll()


print("READY.")


