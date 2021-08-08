FROM python:3.9.6-slim-buster

RUN groupadd user && useradd -m -u 1000 -g user user
USER user

RUN mkdir /home/user/db

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY src /src/
WORKDIR /src

ENV settings_path=/src/
RUN python3 -m unittest

ENTRYPOINT ["python3", "/src/entrypoint.py"]
