## KU Polls: Online Survey Questions 
[![Unit Tests](https://github.com/Sosokker/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/Sosokker/ku-polls/actions/workflows/django.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.2/intro/tutorial01/), with additional features.

## Installation

Here is **[Install Instruction](Installation.md)**.

## How to Run

### Setup.py Method

Using setup.py method, it will set `.env` for you and runserver automatically with [--insecure](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#cmdoption-runserver-insecure).
You can set `DEBUG=True` later and then runserver normally to load static files.

Then, connect to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Manual Installation
After follow all of instruction.
- Set Virtual Environment and Use it.
- Install Dependencies.
- Migrate and then Load fixtures.
- Set variable of `.env`

You can run with this command.

```bash
python manage.py runserver
```

Anyway, if you set `DEBUG = False` then django production server will not load static files for you.
You need to set `DEBUG = True` or run this command.

```bash
python manage.py runserver --insecure
```

Then, connect to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

**NOTE** : If you have problems with port you can use runserver and specific your own port.

For example, If you run this command then you need to connect to [http://127.0.0.1:7000/](http://127.0.0.1:7000/)
```bash
python manage.py runserver 7000
```

## Demo Superuser

|Username|Password|
|:--:|:--:|
|admin|ineedmorebullets|

## Demo User

|Username|Password|
|:--:|:--:|
|tester1|aa12345678aa|
|tester2|aa12345678aa|
|tester3|aa12345678aa|
|tester4|aa12345678aa|
|novote |aa12345678aa|

## Project Documents

All project documents are in the [Project Wiki](https://github.com/Sosokker/ku-polls/wiki).

- [Vision Statement](https://github.com/Sosokker/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/Sosokker/ku-polls/wiki/Requirements)
- [Iteration1](https://github.com/Sosokker/ku-polls/wiki/Iteration-1-Plan)
- [Iteration2](https://github.com/Sosokker/ku-polls/wiki/Iteration-2-Plan)
- [Iteration3](https://github.com/Sosokker/ku-polls/wiki/Iteration-3-Plan)
- [Iteration4](https://github.com/Sosokker/ku-polls/wiki/Iteration-4-Plan)

[Django-Tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
