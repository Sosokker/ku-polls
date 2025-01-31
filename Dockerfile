FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y python3 python3-pip

RUN apt-get install -y python3-venv

WORKDIR /usr/share/ku-polls

COPY . /usr/share/ku-polls

# Create virtual environment, install requirement
RUN python3 -m venv venv \
    && ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install -r requirements.txt

EXPOSE 8000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]