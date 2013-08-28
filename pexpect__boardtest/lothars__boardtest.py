#!/usr/bin/env python

import sys
import os
import re

## at least install pexpect locally and set PYTHONHOME to it, e.g.
#export PYTHONPATH=${PYTHONPATH}:/home/lothar/lib/python2.7/site-packages
import pexpect

## call shell commands
import subprocess

## sleep
from time import sleep


################################################################################
## individual settings

TRASH = "/work/lothar/TESTBUILD_REMOVED/"
USER = "lothar"

################################################################################

   
# TODO classes, and functions using 'self'
# TODO test pexpect implementation and improve
   

## copy2, but does not copy all meta data
#import shutil

class CommandException( Exception ):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)




class ExpectException( Exception ):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)




class ExpectHandler:
    ## attrs
    _shell = None
    _machine = ""
    _uboot_cmds = []
    _boot_cmd = ""

    ## ctor
    def __init__( self, machine ):
        self._shell = None

        self._machine = machine

        ## NFS MANUAL BOOT: m28evk [move to somewhere else, this function in an obj, only should "play" the uboot_cmds]
        self._uboot_cmds = []
        # => setenv serverip 192.168.1.1
        self._uboot_cmds.append( 'setenv serverip 192.168.1.1' )
        # => setenv ipaddr 192.168.20.33
        self._uboot_cmds.append( 'setenv ipaddr 192.168.20.33' )
        # => tftp 0x41000000 /tftpboot/lothar/uImage-m28evk.dtb
        self._uboot_cmds.append( 'tftp 0x41000000 /tftpboot/lothar/uImage-m28evk.dtb' )
        # => tftp 0x42000000 /tftpboot/lothar/uImage
        self._uboot_cmds.append( 'tftp 0x42000000 /tftpboot/lothar/uImage' )
        # => setenv bootargs root=/dev/nfs rw nfsroot=192.168.1.1:/work/lothar/BUILD,v3,tcp
        self._uboot_cmds.append( 'setenv bootargs root=/dev/nfs rw nfsroot=192.168.1.1:/work/lothar/BUILD,v3,tcp' )
        # => setenv bootargs ${bootargs} ip=192.168.20.33:192.168.1.1:192.168.1.254:255.255.0.0:m28:eth0:off
        self._uboot_cmds.append( 'setenv bootargs ${bootargs} ip=192.168.20.33:192.168.1.1:192.168.1.254:255.255.0.0:m28:eth0:off' )
        # => setenv bootargs ${bootargs} console=ttyAMA0,115200
        self._uboot_cmds. append( 'setenv bootargs ${bootargs} console=ttyAMA0,115200' )

        # => bootm 0x42000000 - 0x41000000
        self._boot_cmd = "bootm 0x42000000 - 0x41000000"

    def __str__( self ):
        print "class ExpectHandler:"
        print "_con_power: " + self._con_power
        print "_con_client: " + self._con_client
        print "_machine: " + self._machine

    def _expect_expect( self, cmd = "", exp = [], timeout = 30, warning = "" ):
        if "\n\r" == cmd: print "EXP $> <ENTER>"
        else: print "EXP $> " + cmd
# FIXME catch error situations in u-boot, at initialization (e.g. missing serverip)
        exp = [ pexpect.EOF ] + exp   
#        exp = [ pexpect.EOF, '\*\*\* ERROR\:.*' ] + exp  
#        exp = [ pexpect.EOF, ".*(Error|ERROR|Fail).*" ] + exp  
        ret = self._shell.expect( exp, timeout = timeout )
        if 0 == ret:
#        if 0 == ret or 1 == ret:
            print "-" * 80
            print "command: " + cmd
            message = cmd
            print "-" * 80
            print self._shell
            print "-" * 80
#            message += "%s" % "\n" . join(map(str, self._shell )) 
            if 0 < len( warning ): message += " => CHECK: " + warning
            raise ExpectException( message )

# FIXME: u-boot shell ERROR messages from command A caught at command C or D
#         m = re.search("Error|ERROR|Fail", self._shell.before)
#         if None != m:
#             if 0 < len( m.group( 0 ) ):
#                 die( "FAILED - before" )  
        
#         m = re.search("Error|ERROR|Fail", self._shell.after)
#         if None != m:
#             if 0 < len( m.group( 0 ) ):
#                 die( "FAILED - after" )  
#                 raise ExpectException( message )
        
        return ret

    def _expect_cmd( self, cmd = "", exp = [], timeout = 30, warning = "" ):
#        print "XXX timeout '" + str(timeout) + "'"   
        self._shell = pexpect.spawn( cmd, timeout = timeout, maxread = 5000 )
        return self._expect_expect( cmd, exp, timeout, warning )

    def _expect_cmd_append( self, cmd="", exp=[], warning = "", timeout = 30 ):
        self._shell.sendline( cmd )
        return self._expect_expect( cmd, exp, timeout, warning )

    ## connect with pexpect
    def do_expect_connect( self ):
        if 0 == len( self._machine ): die( "_machine was empty" )

        ## run machine
        self._expect_cmd( "remote_power " + self._machine + " -l", ['.*off'], warning = "is " + self._machine + " already running?" )
        self._expect_cmd( "remote_power " + self._machine + " on", ['Power on   ' + self._machine + ': OK'] )

        ## connect and catch prompt
        self._expect_cmd( "connect " + self._machine
                          , ['### Connect to "' + self._machine + '" using command: /usr/bin/rlogin ts0 -l ' + self._machine ]
                          , timeout = 180 )
        sleep( 2 )
        self._expect_cmd_append( "\n\r", ["=> "] )
        ## if you reached here, you have a powered machine and a prompt

    ## configure uboot
    def do_expect_configure( self ):
        ## play uboot commands
        for cmd in self._uboot_cmds:
            self._expect_cmd_append( cmd, ["=> "] )
# FIXME delay or pexpect.wait() have difficulties with u-boot shell
            sleep( 5 )   


# TODO check timeout settings in expect or in spawn? 
    def do_expect_boot( self ):
        self._expect_cmd_append( self._boot_cmd, [self._machine + " login: "], timeout = 180, warning = "build failed, not bootable via NFS" )
    ## we have booted the machine


    def do_expect_shutdown( self ):
        self._shell.sendline( '~~.' )

        ## give some slight delay, to make sure the command (checkout console) was processed
        sleep( 1 )

        self._shell.kill( 0 )

        ## run machine
        self._expect_cmd( "remote_power " + self._machine + " off", ['Power off  ' + self._machine + ': OK'] )

# TODO
## then run automized tests (cheapest, just boot)
# TODO
    




def die( msg = ""):
    if 0 == len(msg): msg = "I see..."
    print "FATAL: " + msg
    sys.exit( -1 )


def run_cmd( cmd = [] ):
    out = []
    ret = ""
    try:
        print "    $> %s" % " ".join(map( str, cmd ))
        out, ret = subprocess.Popen( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if 0 < len(ret):
            raise CommandException( ret )

    except subprocess.CalledProcessError, err:
        import traceback
        traceback.print_exc()
        die( "" )
    except OSError, err:
        import traceback
        traceback.print_exc()
        die( "" )

    return out


def get_bare_path( dirname, basename ):
    filename = run_cmd( ["readlink", dirname + basename] )
    if 0 == len(filename):
        die( "file not found: '" + dirname + basename + "'")
    return dirname + filename

def do_exists( path ):
    path = path.strip( "\n" )
    return os.path.exists( path )

def do_isfile( path ):
    path = path.strip( "\n" )
    return os.path.isfile( path )

def do_remove( path ):
    path = path.strip( "\n" )
    if path.endswith('/'): path = path[:-1]
    import datetime
    cmd = [ "mv", path, TRASH + str( datetime.datetime.now() ).replace(' ', '-').replace(':','-').split('.')[0] ]
    
    run_cmd( cmd )
    
## TODO for debugging, run this interactively...
    # while True:
    #     try:
    #         aw = raw_input( "apply commend:\n\t'%s'\n(y|n)? "%"' '".join(map( str, cmd )) )
    #         aw = aw[0].lower()
    #         if aw == "y":
    #             run_cmd( cmd )
    #             break
    #         if aw == "n": die("remove the folder manually then...")
    #     except IndexError:
    #         ## input was ''
    #         pass

def do_emptydir( path ):
    path = path.strip( "\n" )
    if do_exists( path ): do_remove( path )
    cmd = ["mkdir", path ]
    run_cmd( cmd )

def do_unpack( source, destination = ""):
    ## unpack
    source = source.strip( "\n" )
    cmd = []
    if ".tar.bz2" == IMAGE_FSTYPE_rootfs or ".tbz" == IMAGE_FSTYPE_rootfs:
        cmd += [ "tar", "-xjf", source ]
    elif ".tar.gz" == IMAGE_FSTYPE_rootfs:
        cmd += [ "tar", "-xzf", source ]
    elif ".tar.xz" == IMAGE_FSTYPE_rootfs:
        cmd += [ "tar", "-xJf", source ]
    # TODO more

    ## avoid stupid errors due to /dev files
    cmd += ["--exclude", "*/dev/*"]

    ## destination set?
    destination = destination.strip( "\n" )
    if 0 < len( destination ):
        cmd += [ "-C", destination ]

    run_cmd( cmd )


def do_save_copy( source, destination, destination_filename ):
    source = source.strip( "\n" )
    destination = destination.strip( "\n" )
    if not do_isfile( source ): die( "source not found: '" + source + "'" )
    if not do_exists( destination ): die( "destination folder not found: '" + destination + "'" )

    ## destination valid?
    if do_isfile( destination + destination_filename ):
        do_remove( destination + destination_filename )

    ## copy file
    cmd = [ "cp", source, destination + destination_filename ]
    run_cmd( cmd )





## START                                                                        
# TODO use __main__ and common python syntax!

# TODO from args
# TODO read out of machine conf
MACHINE = "m28evk"
IMAGE = "core-image-qte-sdk"
KERNEL_IMAGETYPE = "uImage"
BUILD = "TESTBUILD_" + MACHINE + "-" + IMAGE
IMAGE_FSTYPE_rootfs = ".tar.bz2"


## sources
#pth_source = "/work/lothar/" + BUILD + "/tmp/deploy/images/"
pth_source = "/work/lothar/" + BUILD + "/tmp/deploy/images/"

pth_src_kernel_type = get_bare_path( pth_source, KERNEL_IMAGETYPE )
pth_src_kernel_dtb = get_bare_path( pth_source, KERNEL_IMAGETYPE + "-" + MACHINE + ".dtb" )
pth_src_rootfs_tarball = get_bare_path( pth_source, IMAGE + "-" + MACHINE + IMAGE_FSTYPE_rootfs )



## destinations
pth_dst_rootfs = "/work/lothar/BUILD/"
pth_dst_kernel = "/tftpboot/lothar/"


# TODO implement as class...

## setup for rootfs, dtb, etc.
try:
    ## check if target folder exists, in case remove
  
    do_emptydir( pth_dst_rootfs )

    ## unpack/copy (and unpack) into dst_rootfs
  
    do_unpack( pth_src_rootfs_tarball, pth_dst_rootfs )

    ## kernel
  
    do_save_copy( pth_src_kernel_type, pth_dst_kernel, KERNEL_IMAGETYPE )

    ## dtb
  
    do_save_copy( pth_src_kernel_dtb, pth_dst_kernel, KERNEL_IMAGETYPE + "-" + MACHINE + ".dtb" )

    ## connect machine
    exp = ExpectHandler( MACHINE )
    exp.do_expect_connect()
    exp.do_expect_configure()
    exp.do_expect_boot()

    ## if we get here - the build booted
    print "Build OK"   
# TODO log

    ## shutdow
    print "shutting down..."
    exp.do_expect_shutdown()

# TODO

except CommandException:
    import traceback
    traceback.print_exc()
    die()

except ExpectException:
    import traceback
    traceback.print_exc()
    if None != exp: exp.do_expect_shutdown()
    die()

except (KeyboardInterrupt, SystemExit):
    sys.exit( 0 )

except:
    import traceback
    traceback.print_exc()

## load tests
# TODO

## run tests
# TODO


print "READY.\n"
