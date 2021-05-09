#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
# from glob import glob
from setuptools import setup

# import DistUtilsExtra.command.build_extra
# import DistUtilsExtra.command.build_i18n
# import DistUtilsExtra.command.clean_i18n

# to update i18n .mo files (and merge .pot file into .po files):
# ,,python setup.py build_i18n -m''

# silence pyflakes, __VERSION__ is properly assigned below...
__VERSION__ = '1.2'

# for line in open('gbinstall', 'r').readlines():
#     if (line.startswith('__VERSION__')):
#         exec(line.strip())
PROGRAM_VERSION = __VERSION__


def datafilelist(installbase, sourcebase):
    datafileList = []
    for root, subFolders, files in os.walk(sourcebase):
        fileList = []
        for f in files:
            fileList.append(os.path.join(root, f))
        datafileList.append((root.replace(sourcebase, installbase), fileList))
    return datafileList


prefix = sys.prefix


# '{prefix}/share/man/man1'.format(prefix=sys.prefix), glob('data/*.1')),

data_files = [
    (f'{prefix}/share/applications', ['software-station.desktop']),
    (f'{prefix}/etc/sudoers.d', ['sudoers.d/software-station']),
]

# data_files.extend(datafilelist('{prefix}/share/locale'.format(prefix=sys.prefix), 'build/mo'))

# cmdclass ={
#             "build" : DistUtilsExtra.command.build_extra.build_extra,
#             "build_i18n" :  DistUtilsExtra.command.build_i18n.build_i18n,
#             "clean": DistUtilsExtra.command.clean_i18n.clean_i18n,
# }

setup(name="software-station",
      version=PROGRAM_VERSION,
      description="GhostBSD software manager",
      license='BSD',
      author='Eric Turgeon',
      url='https://github/GhostBSD/software-station/',
      package_dir={'': '.'},
      data_files=data_files,
      # install_requires = [ 'setuptools', ],
      py_modules=["software_station_pkg", "software_station_xpm"],
      scripts=['software-station'],)
# cmdclass = cmdclass,
