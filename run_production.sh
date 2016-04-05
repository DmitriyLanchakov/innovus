#!/bin/sh

WORKDIR="/usr/local/www/tomskforum"
PIDFILE="/var/run/tomskforum/tomskforum.pid"

if [ -s ${PIDFILE} ]; then
    kill -QUIT `cat ${PIDFILE}`
    sleep 2
fi

. ${WORKDIR}/env/bin/activate

${WORKDIR}/env/bin/python ${WORKDIR}/application/manage.py run_gunicorn \
    --config=${WORKDIR}/application/unicorn.py \
    --adminmedia=${WORKDIR}/application/media/admin/ \
    --pid=${PIDFILE} \
    --daemon
