FROM python:latest

WORKDIR /bot
COPY . /bot

RUN pip install Flask Flask-SQLAlchemy Flask-Migrate dialogflow psycopg2
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]