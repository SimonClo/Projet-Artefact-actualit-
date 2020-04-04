FROM python:latest

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release
#     of PostgreSQL, ``9.3``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends postgresql

RUN pip3 install --upgrade pip &&\ 
    pip3 install tqdm psycopg2
# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
WORKDIR /app
COPY . /app
RUN python3 scripts/flatten_hierarchy.py "data/L'express"

RUN chown postgres /app
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker &&\
    createdb -O docker artefact_archives &&\
    export PGPASSWORD="docker" &&\
    psql -U docker -p 5432 -h localhost artefact_archives < data_access/db_dumps/init.sql &&\
    python3 scripts/fill_db.py --user docker --password docker --port 5432 --archives "data/L'express" &&\
    pg_dump -U docker -p 5432 -h localhost artefact_archives > ./data_init.sql


FROM postgres:12.1
COPY --from=0 /app/data_init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 5432

ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB artefact_archives