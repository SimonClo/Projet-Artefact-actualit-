from python:latest

WORKDIR /app
COPY . /app

RUN pip install Flask Flask-SQLAlchemy Flask-Migrate

CMD ["flask", "run", "--host=0.0.0.0"]