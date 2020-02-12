FROM postgres:12.1

COPY db_dumps/init.sql /docker-entrypoint-initdb.d/init.sql

ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB artefact_archives