File upload
===========

Requires
--------
* python 3.5

Required packages
-----------------
* python3-pip
* redis-server

Quick start development mode
----------------------------
#### Setup env and install requirements
    $ virtualenv -p python3 .env
    $ source ./.env/bin/activate
    $ pip install -r requirements.txt

Make migrations for suppliers_db and apply them

    $ ./manage.py makemigrations
    $ ./manage.py migrate --database=default
    $ ./manage.py migrate --database=suppliers_db

##### Run server
    ./manage.py runserver 0.0.0.0:8000

##### Run celery
    celery -A config worker -l info

##### In ./config/settings.py for production
* `DATABASES` setting should look like

```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'suppliers_db': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
```


* `SUPPLIERS_TABLES_MANAGED=False` must be `False`
* `DEBUG=False` must be `False`

How to override `settings` module
---------------------------------
Set env variable like that `DJANGO_SETTINGS_MODULE="config.production_settings"`

e.g.

    DJANGO_SETTINGS_MODULE="config.production_settings" ./manage.py runserver 0.0.0.0:8000
