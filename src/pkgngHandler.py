#!/usr/local/bin/python

from subprocess import Popen, PIPE, STDOUT, call


def packagelist(category):
    cmd = "pkg rquery -a '%C/%n : %c' | grep " + category + "/ | grep -v gnome/ | sort"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True)
    lst = pkg_out.stdout.readlines()
    return lst


def softwareVersion(pkg):
    vcmd = "pkg rquery '%v' " + pkg
    output = Popen(vcmd, shell=True, stdout=PIPE, close_fds=True)
    lst = output.stdout.readlines()
    return lst[0].rstrip()

def sotwareComment(pkg):
    ccmd = "pkg rquery '%c' " + pkg
    output = Popen(ccmd, shell=True, stdout=PIPE, close_fds=True)
    lst = output.stdout.readlines()
    return lst[0].rstrip()