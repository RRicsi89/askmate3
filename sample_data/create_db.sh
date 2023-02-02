#!/bin/bash

set -e

if [[ "$(ls -A /data)" ]]; then
    printf "Found database"
    cp -r /var/lib/postgresql/data/pgdata /var/lib/postgresql/data
else
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    CREATE DATABASE askmate;
    GRANT ALL PRIVILEGES ON DATABASE askmate TO postgres;
    \c askmate
    \i askmatepart2-sample-data.sql;
EOSQL
fi