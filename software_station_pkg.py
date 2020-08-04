#!/usr/bin/env python3.6

from subprocess import Popen, PIPE


def available_package_origin():
    cmd = "pkg rquery '%o' | cut -d '/' -f1"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def available_package_list():
    cmd = "pkg rquery '%o:%n:%v:%sh:%c'"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def installed_package_origin():
    cmd = "pkg query '%o' | cut -d '/' -f1"
    pkg_out = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                    universal_newlines=True, encoding='utf-8')
    lst = list(set(pkg_out.stdout.read().splitlines()))
    lst.sort()
    return lst


def installed_package_list():
    cmd = "pkg query '%o:%n:%v:%sh:%c'"
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
            'name': pi[1],
            'version': pi[2],
            'size': pi[3],
            'comment': pi[4],
            'installed': boolean
        }
        pkg_dict[pl[0]].update({pi[1]: pkg_info})
        pkg_dict['all'].update({pi[1]: pkg_info})
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
            'name': pi[1],
            'version': pi[2],
            'size': pi[3],
            'comment': pi[4],
            'installed': True
        }
        pkg_dict[pl[0]].update({pi[1]: pkg_info})
        pkg_dict['all'].update({pi[1]: pkg_info})
    return pkg_dict


def search_packages(search):
    cmd = f"pkg search -Q name {search} | grep 'Name  ' | cut -d : -f2 | " \
        "cut -d ' ' -f2"
    output = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                   universal_newlines=True, encoding='utf-8')
    lst = output.stdout.read().splitlines()
    return lst


def delete_packages(pkg):
    cmd = f"pkg delete -y {pkg}"
    fetch = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                  universal_newlines=True, encoding='utf-8')
    return fetch.stdout


def fetch_packages(pkg):
    cmd = f"pkg fetch -y {pkg}"
    fetch = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                  universal_newlines=True, encoding='utf-8')
    return fetch.stdout


def install_packages(pkg):
    cmd = f"pkg install -y {pkg}"
    fetch = Popen(cmd, shell=True, stdout=PIPE, close_fds=True,
                  universal_newlines=True, encoding='utf-8')
    return fetch.stdout


def get_pkg_to_install_output(packages):
    pkg_upgrade = Popen(
        f'pkg install -n {packages}',
        shell=True,
        stdout=PIPE,
        close_fds=True,
        universal_newlines=True,
        encoding='utf-8'
    )
    return pkg_upgrade.stdout.read()


def get_pkg_to_remove_output(packages):
    pkg_upgrade = Popen(
        f'pkg delete -n {packages}',
        shell=True,
        stdout=PIPE,
        close_fds=True,
        universal_newlines=True,
        encoding='utf-8'
    )
    return pkg_upgrade.stdout.read()


def get_pkg_changes_data(remove_list, install_list):
    install_pkg = get_pkg_to_install_output(' '.join(install_list))
    install_pkg_list = install_pkg.splitlines()
    remove_pkg = get_pkg_to_remove_output(' '.join(remove_list))
    remove_pkg_list = remove_pkg.splitlines()
    pkg_to_remove = []
    pkg_to_upgrade = []
    pkg_to_install = []
    pkg_to_reinstall = []
    stop = False
    if 'REMOVED:' in remove_pkg:
        for line in remove_pkg_list:
            if 'REMOVED:' in line:
                stop = True
            elif stop is True and line == '':
                stop = False
                break
            elif stop is True:
                pkg_to_remove.append(line.strip())
    if 'UPGRADED:' in install_pkg:
        for line in install_pkg_list:
            if 'UPGRADED:' in line:
                stop = True
            elif stop is True and line == '':
                stop = False
                break
            elif stop is True:
                pkg_to_upgrade.append(line.strip())
    if ' INSTALLED:' in install_pkg:
        for line in install_pkg_list:
            if ' INSTALLED:' in line:
                stop = True
            elif stop is True and line == '':
                stop = False
                break
            elif stop is True:
                pkg_to_install.append(line.strip())
    if 'REINSTALLED:' in install_pkg:
        for line in install_pkg_list:
            if 'REINSTALLED:' in line:
                stop = True
            elif stop is True and line == '':
                stop = False
                break
            elif stop is True:
                pkg_to_reinstall.append(line.strip())
    pkg_dictionaire = {
        'remove': pkg_to_remove,
        'upgrade': pkg_to_upgrade,
        'install': pkg_to_install,
        'reinstall': pkg_to_reinstall
    }
    return pkg_dictionaire
