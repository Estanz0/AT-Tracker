#! /bin/sh

for file in ./db_create_tables/*; do
    psql buses -f "$file"
done

psql buses -f "./db_permissions.sql"