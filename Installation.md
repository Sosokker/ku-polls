## Installation

There are two ways to install and run this project.

1. Use `setup.py` or `setup.ps1`(for windows) to install the project.
2. Manually install the project with the Instruction in section 2.

### 1. Use `setup.py` or `setup.ps1`(for windows) to install the project.
1. Install [Python 3.11 or later](https://www.python.org/downloads/)
2. Clone this repository and Run `setup.py` to install and run the project

**Don't forget to answer the question from `setup.py` to setup the project**

This method will autogenerate Environment Variable for you.
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

### 2. Manually install the project with this instruction.

1. Install [Python 3.11 or later](https://www.python.org/downloads/)
2. Run these commands to clone this repository and enter the directory.
```bash
git clone https://github.com/Sosokker/ku-polls
cd ku-polls
```

3. (Optional: You can use venv instead)Install virtualenv via pip

```bash
python -m pip install --user virtualenv
```
4. Create virtual environment with `venv` or `virtualenv`.
```bash
python -m virtualenv venv
or
python -m venv venv
```
5. Use `virtual environment`

- Windows
```bash
.\venv\Scripts\activate
```

- Linux or MacOS
```bash
source venv/bin/activate
```
6. Install require module.
```
pip install -r requirements.txt
```

7. Create file call `.env` in `ku-polls` directory and add this line
**You can look at `sample.env` for more information and others environment variables to set.**
```bash
SECRET_KEY=your_secret_key
DEBUG = False
ALLOWED_HOSTS = *.ku.th, localhost, 127.0.0.1, ::1
TIME_ZONE = Asia/Bangkok
EMAIL_HOST_PASSWORD = yourpassword
```

You can generate your own `your_secret_key` by this command
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
or 
- [Django Secret Key Generator #1](https://djecrety.ir/)
- [Django Secret Key Generator #2](https://miniwebtool.com/django-secret-key-generator/)

**Don't forget to change `your_secret_key` to your secret key (without quote)**

8. Migrate database and load data into it then runserver.
```bash
python manage.py migrate
python manage.py loaddata data/users.json
python manage.py loaddata data/polls.json
python manage.py loaddata data/vote.json
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
