FROM python:3.12-slim

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

# install gunicorn...
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./lib ./lib

COPY ./settings.py .
COPY ./common.py .
COPY ./main.py .
COPY ./app.py .

COPY ./static ./static
COPY ./templates ./templates

EXPOSE 5000

# use wsgi server to run the flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
