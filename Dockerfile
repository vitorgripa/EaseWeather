FROM python:3.10-bullseye

WORKDIR /app

RUN apt update -y

COPY requirements.txt /tmp/pip-tmp/

RUN pip3 install --no-cache-dir --upgrade -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

COPY ./* /app/

CMD uvicorn main:app --host 0.0.0.0 --port $PORT