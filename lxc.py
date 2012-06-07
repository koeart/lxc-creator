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
import ConfigParser

"""About

Right now all variables are hardcoded, unfortunately.
No checks yet if everything is installed and working.
To check whether your kernel supports lxc please run lxc-checkconfig.
You should have lvm installed and running.

A lv will be created in your current vg. Find out about your VG root name by running `vgdisplay | grep "VG Name"`
Save this under $VG_Name.

The name for your lxc container will be the name for your lv as well.
"""

def main(argv=None):
    """
    this is some stub for our later to-be-used main function. Right now, I'm still testing, so FIXME!!!!
    """

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

def import_config(configfile):
    """
    this imports the global configuration file.
    
    It has a [global] section, containing a 'name' for our container, the filesystemtype 'fs_type', a volumegroup name 'vg_name', the desired logical size 'lv_size' and last but not least some mount path 'mount_path'.
    The [extern] section can provide links to other configuration files and scripts we depend upon or want to use.
    """

    config = ConfigParser.RawConfigParser()
    config.read([configfile])
    return config

def lv_find_current_vg():
    """
    this finds the vg we are into right now and returns it
    """

    p = sub.Popen(["vgdisplay"], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        out = p.stdout.readlines()
        vg_name = out[1].split()[2]
        print "VG Name: " + vg_name
    except:
        print "Fehler! " + p.stderror.read()
    return vg_name

def lv_create():
    """
    here we create our logical volume for the new container.
    we give it a lv_size, a name and a volume group.
    """

    p = sub.Popen(["lvcreate", "-L" + LV_SIZE, "-n"+ LV_NAME, VG_NAME], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        print p.stdout.read()
    except:
        print "Fehler!" + p.stderror.read()

def create_fs():
    """
    here we create a new filesystem for our logical volume. important so we can install some linux distro into it.
    """

    p = sub.Popen(["mkfs."+__self__.FS_TYPE, "dev/"+__self__.VG_NAME+"/"+__self__.LV_NAME], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        print p.stdout.read()
    except:
        print "Fehler! " + p.stderror.read()

def create_sample_config():
    """
    this function simply creates a simple sample config. In case you want to test this stuff, but don't have a config at hand or don't know what to setup.
    """


if __name__ == "__main__":
    sys.exit(main())
    print "hello world"
    print locales()
    sys.exit()

