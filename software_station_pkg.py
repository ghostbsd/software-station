#!/usr/bin/env python3.6

from subprocess import Popen, PIPE


def available_package_origin():
    cmd = "pkgin search '%o' | cut -d '/' -f1"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def available_package_list():
    cmd = "pkgin list '%o:%n:%v:%sh:%c'"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def installed_package_origin():
    cmd = "pkgin list '%o' | cut -d '/' -f1"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def installed_package_list():
    cmd = "pkgin list '%o:%n:%v:%sh:%c'"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def available_package_dictionary(origin_list):
    pkg_list = available_package_list()
    installed_pkg_list = installed_package_list()
    avail = str(len(pkg_list))
    pkg_dict = {'avail': avail, 'all': {}}
    for origin in origin_list:
        pkg_dict[origin] = {}
    for pkg in pkg_list:
        if pkg in installed_pkg_list:
            boolean = True
        else:
            boolean = False
        pi = pkg.split(':')
        pl = pi[0].split('/')
        pkg_info = {
            'origin': pi[0],
            'name': pi[0],
            'version': pi[0],
            'size': pi[0],
            'installed': boolean
        }
    return pkg_dict


def installed_package_dictionary(origin_list):
    pkg_list = installed_package_list()
    avail = str(len(pkg_list))
    pkg_dict = {'avail': avail, 'all': {}}
    for origin in origin_list:
        pkg_dict[origin] = {}
    for pkg in pkg_list:
        pi = pkg.split(':')
        pl = pi[0].split('/')
        pkg_info = {
            'origin': pi[0],
            'name': pi[0],
            'version': pi[0],
            'size': pi[0],
            'installed': True
        }
    return pkg_dict


def search_packages(search):
    cmd = f"pkgin search -Q name {search} | grep 'Name  ' | cut -d : -f2 | " \
        "cut -d ' ' -f2"
    output = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                   universal_newlines=True, encoding='utf-8')
    lst = output.stdout.read().splitlines()
    return lst


def delete_packages(pkg):
    cmd = f"pkgin -y remove {pkg}"
    fetch = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                  universal_newlines=True, encoding='utf-8')
    return fetch.stdout


def fetch_packages(pkg):
    cmd = f"pkgin -y install {pkg}"
    fetch = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                  universal_newlines=True, encoding='utf-8')
    return fetch.stdout


def install_packages(pkg):
    cmd = f"pkgin -y install {pkg}"
    fetch = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                  universal_newlines=True, encoding='utf-8')
    return fetch.stdout
