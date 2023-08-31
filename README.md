## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.2/intro/tutorial01/), with additional features.

## Install and Run

1. Install [Python 3.11.4 or later](https://www.python.org/downloads/)
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

4. Run these commands
```bash
python manage.py migrate
python manage.py loaddata data/polls-v1.json
python manage.py loaddata data/user.json
python manage.py runserver
```
Then connect to `http://127.0.0.1:8000/` or `localhost:8000/`

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

## Project Documents

All project documents are in the [Project Wiki](https://github.com/Sosokker/ku-polls/wiki).

- [Vision Statement](https://github.com/Sosokker/ku-polls/wiki/Vision-Statement)
- [Requirements](https://github.com/Sosokker/ku-polls/wiki/Requirements)

[django-tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)