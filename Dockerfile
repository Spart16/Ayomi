FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install Flask Jinja2 Flask-WTF email-validator Flask-SQLAlchemy
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
