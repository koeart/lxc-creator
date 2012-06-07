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



dev main(argv=None):
    if argv is None:
        argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(argv[1:], "h", ["help"])
            except getopt.error, msg:
                raise Usage(msg)
            # more code, unchanged
        except Usage, err:
            print >>sys.stderr, err.msg
            print >>sys.stderr, "for help use --help"
    return 2

def lv_find_vg():
    p = sub.Popen(["vgdisplay"], shell=false, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        out = p.stdout.readlines()
        output = out[1].split()[2]
        print "VG Name: " + output
        VG_NAME = output
    except:
        print "Fehler! " + p.stderror.read()

def lv_create():
    p = sub.Popen(["lvcreate", "-L" + LV_SIZE, "-n"+ LV_NAME, VG_NAME], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        print p.stdout.read()
    except:
        print "Fehler!" + p.stderror.read()

def create_fs():
    p = sub.Popen(["mkfs."+FS_TYPE, "dev/"+VG_NAME+"/"+LV_NAME], shell=false, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        print p.stdout.read()
    except:
        print "Fehler! " + p.stderror:read()


if __name__ == "__main__":
    sys.exit(main())
    print "hello world"
    
