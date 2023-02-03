#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    CREATE DATABASE askmate;
    GRANT ALL PRIVILEGES ON DATABASE askmate TO postgres;
    \c askmate
    \i askmatepart2-sample-data.sql;
EOSQL
