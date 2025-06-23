#!/usr/bin/env sh

cp -f software-station software-station.py

xgettext software-station.py -o po/software-station.pot

msgmerge -U po/zh_CN.po po/software-station.pot
msgmerge -U po/fr.po po/software-station.pot
msgmerge -U po/pt_br.po po/software-station.pot
msgmerge -U po/ru.po po/software-station.pot

rm software-station.py