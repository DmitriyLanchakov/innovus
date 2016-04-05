
#!/usr/bin/env bash
source ../env/bin/activate

PIDFILE=${VIRTUAL_ENV}/tomskforum.pid


if [ -s ${PIDFILE} ]; then
    kill -QUIT `cat ${PIDFILE}`
    sleep 2
fi

python manage.py thumbnail clear

python manage.py run_gunicorn \
    --bind=0.0.0.0:8000 \
    --workers=4 \
    --debug \
    --preload \
    --adminmedia=media/admin/ \
    --pid=${PIDFILE}

