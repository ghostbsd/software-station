#!/usr/local/bin/python3.6

from subprocess import Popen, PIPE


def package_origin():
    cmd = "pkg rquery '%o' | cut -d '/' -f1"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True)
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def package_list():
    cmd = "pkg rquery -a '%o:%n:%c'"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True)
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def package_dictionary(origin_list):
    pkg_list = package_list()
    avail = str(len(pkg_list))
    pkg_dict = {'avail': avail, 'all': {}}
    for origin in origin_list:
        pkg_dict[origin] = {}
    for pkg in pkg_list:
        pi = pkg.split(':')
        pl = pi[0].split('/')
        pkg_dict[pl[0]].update({pi[1]: pi[2]})
        pkg_dict['all'].update({pi[1]: pi[2]})
    return pkg_dict


def packagelist(category):
    cmd = "pkg rquery -a '%o:%c' | grep " + category + "/ | sort"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True)
    lst = pkg_out.stdout.readlines()
    return lst


def softwareversion(pkg):
    vcmd = "pkg rquery '%v' " + pkg
    output = Popen(vcmd, shell=True, stdout=PIPE, close_fds=True,
                   universal_newlines=True)
    lst = output.stdout.readlines()
    return lst[0].rstrip()


def sotwarecomment(pkg):
    ccmd = "pkg rquery '%c' " + pkg
    output = Popen(ccmd, shell=True, stdout=PIPE, close_fds=True,
                   universal_newlines=True)
    lst = output.stdout.readlines()
    return lst[0].rstrip()


def pkgsearch(search):
    cmd = f"pkg search {search}"
    output = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                   universal_newlines=True)
    lst = output.stdout.read().splitlines()
    return lst
