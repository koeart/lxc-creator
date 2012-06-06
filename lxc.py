#!/usr/bin/env python

# configure an lxc container using python
# by Paul Schwanse
# koeart@zwoelfelf.net
# Licensed under GPL

"""Module docstring.

This serves as a long usage message.
"""
import sys
import getopt
import subprocess as sub

"""About

Right now all variables are hardcoded, unfortunately.
No checks yet if everything is installed and working.
To check whether your kernel supports lxc please run lxc-checkconfig.
You should have lvm installed and running.

A lv will be created in your current vg. Find out about your VG root name by running `vgdisplay | grep "VG Name"`
Save this under $VG_Name.

The name for your lxc container will be the name for your lv as well.
"""

NAME='test1'
FS_TYPE='ext3'
VG_NAME='rodriguez' #your root vg name
LV_NAME=NAME + '_root' #name for the new LXC Container
LV_SIZE='1G' #we are using the lv-create options, everthing they take as size input is fine
MOUNT_PATH='/lxc/' + LV_NAME

# and now for the config files
LXC_CONFIG_PATH='configs/lxc-debian'
MOUNT_CONFIG='configs/mount-options' #this should be a single line which will be added to /etc/fstab




def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

def lv_create():
    process = sub.Popen(["lvcreate", "-L" + LV_SIZE, "-n"+ LV_NAME, VG_NAME], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    print process.communicate()

if __name__ == "__main__":
    main()
    print "hello world"
    lv_create()
    
