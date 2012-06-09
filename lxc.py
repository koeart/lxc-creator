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
    
    config = ConfigParser.SafeConfigParser()
    config.read([configfile])
    return config

def lv_find_current_vg():
    """
    this finds the vg we are into right now and returns it
    """

    p = sub.Popen(["vgdisplay"], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        #vgdisplay gives you a lot of information
        out = p.stdout.readlines()
        # we just need the second line and then - the third argument in the list
        vg_name = out[1].split()[2]
        print "VG Name: " + vg_name
        return vg_name
    except:
        print "Fehler! " + p.stderror.read()
        return NULL

def lv_create(lv_size, lv_name, vg_name):
    """
    here we create our logical volume for the new container.
    we give it a lv_size, a name and a volume group.
    """

    p = sub.Popen(["lvcreate", "-L" + lv_size, "-n"+ lv_name, vg_name], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        print p.stdout.read()
        return True
    except:
        print "Fehler!" + p.stderror.read()
        return False

def create_fs(fs_type, vg_name, lv_name):
    """
    here we create a new filesystem for our logical volume. important so we can install some linux distro into it.
    """

    p = sub.Popen(["mkfs."+ fs_type, "/dev/mapper/"+ vg_name+"-"+ lv_name + "_root"], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    try:
        print p.stdout.read()
        print p.stderr.read()
        return True
    except:
        print "Fehler! " + p.stderror.read()
        return False

def mount_lv(vg_name, lv_name, dev_path, mount_path):
    """
    here the logical volume gets mounted.
    both, dev_path and mount_path can be found in the globalconfig.cfg file
    """

    p = sub.Popen(["mount", "-t","auto", dev_path, mount_path], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    print "stdout: " + p.stdout.read()
    print "Error: " + p.stderr.read()
   
def create_lxc(lxc_name, lxc_script, mount_path):
    """
    here we create (and install) the actual lxc-container system.
    one can specify a lxc_script (f.e. from /usr/lib/lxc/templates/)
    
    lxc-scripte nehmen folgende Parameter auf: rootfs and a hostname
    """

    p = sub.Popen(["/usr/lib/lxc/templates/"+ lxc_script, "-p", mount_path], shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
    print "Fertig: " + p.stdout.read()
    print "Fehler: " + p.stderr.read()

    return True

def create_sample_config():
    """
    this function simply creates a simple sample config. In case you want to test this stuff, but don't have a config at hand or don't know what to setup.
    FIXME: Polish it, so sample configuration looks for volume group name and stuff like this
    Here is it's should-be content:

        [global]
        name = name_of_container
        fs_type = ext3 # or some other
        vg_name = name_of_volumegroup
        lv_size = 4G # desired size
        mount_path = /lxc/ # your favorite mount-path for the container

        [extern]
        lxc_config = /usr/lib/lxc/templates/lxc-debian #your favorit lxc-install script
        mount_config = ./configs/mount-options
    """
    config = ConfigParser.RawConfigParser()
    config.add_section('extern')
    config.add_section('global')
    config.set('extern', 'mount_config', './mount-options')
    config.set('extern', 'lxc_config', '/usr/lib/lxc/templates/lxc-debian')
    config.set('global', 'mount_path', '/lxc/')
    config.set('global', 'lv_size', '4G')
    config.set('global', 'vg_name', 'rodriguez')
    config.set('global', 'fs_type', 'ext3')
    config.set('global', 'name', 'test1')

    with open('./configs/globalconfig.cfg', 'wb') as globalconfig:
        config.write(globalconfig)
    return True


if __name__ == "__main__":
    sys.exit(main())
    print "hello world"
    print locales()
    sys.exit()

