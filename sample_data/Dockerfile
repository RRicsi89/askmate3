FROM postgres:15
COPY create_db.sh docker-entrypoint-initdb.d/
COPY askmatepart2-sample-data.sql .
EXPOSE 5432
