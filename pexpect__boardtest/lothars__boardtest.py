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

MY__TRASH = "/work/lothar/TESTBUILD_REMOVED/" ## move to trash folder, instead of remove directly (if so, set this to "")
#MY__USER = "lothar" 
MY__WORKDIR = "/work/lothar/"
MY__TFTPDIR = "/tftpboot/lothar/"
MY__KERNEL_IMAGETYPE = "uImage"
MY__IMAGE = "core-image-qte-sdk"
MY__IMAGE_FSTYPE_rootfs = ".tar.bz2"

## machine specific, here for m28evk (better, comes from config files, yocto, etc.)
MY__MACHINE = "m28evk"
MY__uboot_cmds = []
MY__uboot_cmds.append( 'setenv serverip 192.168.1.1' )
MY__uboot_cmds.append( 'setenv ipaddr 192.168.20.33' )
MY__uboot_cmds.append( 'tftp 0x41000000 /tftpboot/lothar/uImage-m28evk.dtb' )
MY__uboot_cmds.append( 'tftp 0x42000000 /tftpboot/lothar/uImage' )
MY__uboot_cmds.append( 'setenv bootargs root=/dev/nfs rw nfsroot=192.168.1.1:/work/lothar/BUILD,v3,tcp' )
MY__uboot_cmds.append( 'setenv bootargs ${bootargs} ip=192.168.20.33:192.168.1.1:192.168.1.254:255.255.0.0:m28:eth0:off' )
MY__uboot_cmds.append( 'setenv bootargs ${bootargs} console=ttyAMA0,115200' )
MY__boot_cmd = "bootm 0x42000000 - 0x41000000"

################################################################################

#TODO: remove delay quickfixes by using appropriate pexpect flag settings
#TODO: use pexpect logging
#TODO: improve pexpect evaluation of before/after/buffer & Co
#TODO: try reading values from yocto, config files, e.g. DUTS machine configs (use of PATH?)
#TODO: implement 'class Boardtest'
#TODO: try implementing tree structure for test suites (starting as list)
#TODO: try reading test scripts from DUTS and set up tests
#TODO: try to find solution fro interaction test setups
#TODO: try to find solution for async interaction test setup
#etc etc etc

def die( msg = ""):
    if 0 == len(msg): msg = "I see..."
    print "FATAL: " + msg
    sys.exit( -1 )



## some exceptions
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


## machine
# TODO in case set up list of Machine objects
# TODO make Machine objects readout corresponding config files automatically
class Machine( object ):
    _machinename = ""
    _uboot_cmds = []
    _boot_cmd = ""

    def __init__( self, machinename ):
# TODO test
        if str is not type(machinename): die("wrong type passed, a string is needed here")
        self._machinename = machinename

# TODO read from config
        self._uboot_cmds = MY__uboot_cmds

# TODO read from config
        self._boot_cmd = MY__boot_cmd

    def __str__( self ):
        return self._machinename

    def uboot_cmds( self ): return self._uboot_cmds
    def boot_cmd( self ): return self._boot_cmd



class ExpectHandler( object ):
    ## attr
    _shell = None
    _machine = None

    ## ctor
    def __init__( self, machine ):
        self._shell = None
# TODO test for machine object   
        if type( machine ) != Machine: die( "wrong type passed for machine, a object of Machine is needed, while '" + type( machine ) + "' was passed" )
        self._machine = machine

    def __str__( self ):
        print "class ExpectHandler:"
        print "_machine: " + str(self._machine)

    ## func
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
        if 0 == len( str(self._machine) ): die( "_machine was empty" )

        ## run machine
        self._expect_cmd( "remote_power " + str(self._machine) + " -l", ['.*off'], warning = "is " + str(self._machine) + " already running?" )
        self._expect_cmd( "remote_power " + str(self._machine) + " on", ['Power on   ' + str(self._machine) + ': OK'] )

        ## connect and catch prompt
        self._expect_cmd( "connect " + str(self._machine)
                          , ['### Connect to "' + str(self._machine) + '" using command: /usr/bin/rlogin ts0 -l ' + str(self._machine) ]
                          , timeout = 180 )
        sleep( 2 )
        self._expect_cmd_append( "\n\r", ["=> "] )
        ## if you reached here, you have a powered machine and a prompt

    ## configure uboot
    def do_expect_configure( self ):
        ## play uboot commands
        for cmd in self._machine.uboot_cmds():
            self._expect_cmd_append( cmd, ["=> "] )
# FIXME delay or pexpect.wait() have difficulties with u-boot shell
            sleep( 5 )   


# TODO check timeout settings in expect or in spawn? 
    def do_expect_boot( self ):
        self._expect_cmd_append( self._machine.boot_cmd(), [str(self._machine) + " login: "], timeout = 180, warning = "build failed, not bootable via NFS" )
    ## we have booted the machine


    def do_expect_shutdown( self ):
        self._shell.sendline( '~~.' )

        ## give some slight delay, to make sure the command (checkout console) was processed
        sleep( 1 )

        self._shell.kill( 0 )

        ## run machine
        self._expect_cmd( "remote_power " + str(self._machine) + " off", ['Power off  ' + str(self._machine) + ': OK'] )

# TODO automized tests, as list/tree of test objects (cheapest, just boot)




class System( object ):
    ## attr
    _machine = None

    ## ctor
    def __init__( self, machine ):
        if Machine is not type( machine ): die("wrong type passed, needs to be Machine object and not '" + type( machine ) + "'")
        self._machine = machine
        self._IMAGE = ""
        self._KERNEL_IMAGETYPE = ""
        self._BUILD = ""
        self._IMAGE_FSTYPE_rootfs = ""
        self._pth_source = ""
        self._pth_src_kernel_type = ""
        self._pth_src_kernel_dtb = ""
        self._pth_src_rootfs_tarball = ""
        self._pth_dst_rootfs = ""
        self._pth_dst_kernel = ""
        ## init values
        self._initialize()

    ## getter
    def MACHINE( self ): return self._machine
    def IMAGE( self ): return self._IMAGE
    def KERNEL_IMAGETYPE( self ): return self._KERNEL_IMAGETYPE
    def BUILD( self ): return self._BUILD
    def IMAGE_FSTYPE( self ): return self._IMAGE_FSTYPE_rootfs

    ## func
    def _initialize( self ):
# TODO read out of machine conf by self._machine as only given argument (possible?)
# TODO read from config
        self._IMAGE = MY__IMAGE
# TODO read from config
        self._KERNEL_IMAGETYPE = MY__KERNEL_IMAGETYPE
# TODO read from config
        self._IMAGE_FSTYPE_rootfs = MY__IMAGE_FSTYPE_rootfs
        self._BUILD = "TESTBUILD_" + str(self.MACHINE()) + "-" + self.IMAGE()
        ## sources
        self._pth_source = MY__WORKDIR + self.BUILD() + "/tmp/deploy/images/"
        ## source and destination paths on system
        self._pth_src_kernel_type = self._strip_path( self._pth_source, self.KERNEL_IMAGETYPE() )
# TODO read from config if dtb is to be built or not
        self._pth_src_kernel_dtb = self._strip_path( self._pth_source, self.KERNEL_IMAGETYPE() + "-" + str(self.MACHINE()) + ".dtb" )
        self._pth_src_rootfs_tarball = self._strip_path( self._pth_source, self.IMAGE() + "-" + str(self.MACHINE()) + self.IMAGE_FSTYPE() )
        ## destinations
        self._pth_dst_rootfs = MY__WORKDIR + "BUILD/"
        self._pth_dst_kernel = MY__TFTPDIR

    def _strip_path( self, dirname, basename ):
        filename = self.run_cmd( ["readlink", dirname + basename] )
        if 0 == len(filename):
            die( "file not found: '" + dirname + basename + "'")
        return dirname + filename

    def _path_exists( self, path ):
        path = path.strip( "\n" )
        return os.path.exists( path )

    def _path_isfile( self, path ):
        path = path.strip( "\n" )
        return os.path.isfile( path )

    def prepare( self ):
        ## check if target folder exists, in case remove
        self.do_emptydir( self._pth_dst_rootfs )

        ## unpack/copy (and unpack) into dst_rootfs
        self.do_unpack( self._pth_src_rootfs_tarball, self._pth_dst_rootfs )

        ## kernel
        self.do_save_copy( self._pth_src_kernel_type, self._pth_dst_kernel, self.KERNEL_IMAGETYPE() )

        ## dtb
        self.do_save_copy( self._pth_src_kernel_dtb, self._pth_dst_kernel, self.KERNEL_IMAGETYPE() + "-" + str(self.MACHINE()) + ".dtb" )

    def run_cmd( self, cmd = [] ):
        ## import shutil / copy2 not used here, because does not copy all meta data
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

    def do_remove( self, path ):
        path = path.strip( "\n" )
        if path.endswith('/'): path = path[:-1]
        import datetime
## TODO better remove directly, for safety here - just moving to a TRASH folder
        cmd = [ "mv", path, MY__TRASH + str( datetime.datetime.now() ).replace(' ', '-').replace(':','-').split('.')[0] ]
## TODO interactive mode for debugging, in case implement separate "interactive" mode...
        while True:
            try:
                aw = raw_input( "apply commend:\n\t'%s'\n(y|n)? "%"' '".join(map( str, cmd )) )
                aw = aw[0].lower()
                if aw == "y":
                    run_cmd( cmd )
                    break
                if aw == "n": die("remove the folder manually then...")
            except IndexError:
                ## input was ''
                pass
## ...or, simply turn it off and procede right away w/ the command
        #self.run_cmd( cmd )
##

    def do_emptydir( self, path ):
        path = path.strip( "\n" )
        if self._path_exists( path ): self.do_remove( path )
        cmd = ["mkdir", path ]
        self.run_cmd( cmd )

    def do_unpack( self, source, destination = ""):
        source = source.strip( "\n" )
        cmd = []
        if ".tar.bz2" == self.IMAGE_FSTYPE() or ".tbz" == self.IMAGE_FSTYPE():
            cmd += [ "tar", "-xjf", source ]
        elif ".tar.gz" == self.IMAGE_FSTYPE():
            cmd += [ "tar", "-xzf", source ]
        elif ".tar.xz" == self.IMAGE_FSTYPE():
            cmd += [ "tar", "-xJf", source ]
# TODO more more more

        ## avoid stupid errors due to /dev files
        cmd += ["--exclude", "*/dev/*"]

        ## destination set?
        destination = destination.strip( "\n" )
        if 0 < len( destination ):
            cmd += [ "-C", destination ]

        self.run_cmd( cmd )


    def do_save_copy( self, source, destination, destination_filename ):
        source = source.strip( "\n" )
        destination = destination.strip( "\n" )
        if not self._path_isfile( source ): die( "source not found: '" + source + "'" )
        if not self._path_exists( destination ): die( "destination folder not found: '" + destination + "'" )

        ## destination valid?
        if self._path_isfile( destination + destination_filename ):
            self.do_remove( destination + destination_filename )

        ## copy file
        cmd = [ "cp", source, destination + destination_filename ]

        self.run_cmd( cmd )





## START                                                                        
# TODO use __main__ and common python syntax!

# TODO implement as class...
if __name__ == "__main__":
    ## setup for rootfs, dtb, etc.
    try:
# TODO list of machiens

        ## init machine
        mach = Machine( MY__MACHINE )

        ## prepare system for machine
        sys = System( mach )
        sys.prepare()

        ## connect machine
        exp = ExpectHandler( mach )
        exp.do_expect_connect()
        exp.do_expect_configure()
        exp.do_expect_boot()

        ## run tests
# TODO process list of Test objects

        ## if we get here - the build booted
        print "Build OK"   
# TODO better report to a log file or something

        ## shutdow
        print "shutting down..."
        exp.do_expect_shutdown()

# TODO improve what to do in case of exception
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


print "READY.\n"
