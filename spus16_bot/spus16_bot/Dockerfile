FROM python:3.8

RUN apt-get -y update && apt-get install -y sqlite3 libsqlite3.dev

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./hello.py" ]