## KU Polls: Online Survey Questions 
[![Unit Tests](https://github.com/Sosokker/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/Sosokker/ku-polls/actions/workflows/django.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.2/intro/tutorial01/), with additional features.

## Install and Run
### Run Setup.py (Recommended)
1. Install [Python 3.11 or later](https://www.python.org/downloads/)
2. Clone this repository and Run `setup.py` to install and run the project

**Don't forget to answer the question from `setup.py` to setup the project**
```bash
git clone https://github.com/Sosokker/ku-polls
cd ku-polls
python setup.py
```
If you want to customize the environment variables, name of environment folder then run this command
```bash
python setup.py -custom
```
or run `setup.ps1` (For Windows User)

----

### Manual Installation (If the above method doesn't work)
1. Install [Python 3.11 or later](https://www.python.org/downloads/)
2. Run these commands to clone and install requirements.txt
```bash
git clone https://github.com/Sosokker/ku-polls
cd ku-polls
pip install -r requirements.txt
```
3. Create file call `.env` in `ku-polls` directory and add this line
```bash
SECRET_KEY=your_secret_key
```

You can generate your own `your_secret_key` by this command
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
or 
- [Django Secret Key Generator #1](https://djecrety.ir/)
- [Django Secret Key Generator #2](https://miniwebtool.com/django-secret-key-generator/)

**Don't forget to change `your_secret_key` to your secret key (without quote)**

**You can look at `sample.env` for more information and others environment variables to set.**

4. Run these commands
```bash
python manage.py migrate
python manage.py loaddata data/users.json
python manage.py loaddata data/polls.json
python manage.py runserver
```

***NOTE***

By Default `DEBUG=False` and Django will not load Static files for you so if you want to apply CSS run this.
```bash
python manage.py runserver --insecure
```
or set `DEBUG=True`
or do the [collectstatic](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/)

Then connect to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [localhost:8000/](localhost:8000/)

----

**Recommend**

You can create virtual environment by using this command before install requirements.txt

1. Install virtualenv via pip

```bash
python -m pip install --user virtualenv
```
2. Run these commands
```bash
python -m virtualenv .venv
```
3. Use `virtual environment`
```bash
.venv\Scripts\activate
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

[django-tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
