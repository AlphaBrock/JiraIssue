#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cwd=$(pwd)

sed -i "s#\/data#${cwd}#g" ${cwd}/uwsgi.ini
uwsgi --ini ${cwd}/uwsgi.ini

