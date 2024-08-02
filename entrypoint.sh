#!/bin/sh
if [ "$DB_HOSTNAME" = "postgresql_db" ]
then
echo "Waiting for Postgres..."
while ! nc -z $DB_HOSTNAME $DB_PORT; do
sleep 0.1
done
echo "PostgreSQL started"
fi
python manage.py migrate
exec "$@"