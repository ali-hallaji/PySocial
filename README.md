<p align="center">
  <a href="http://pysocial.com">
    <img alt="PySocial" src="static/main/img/logo.png">
  </a>
</p>
<a href='http://pysocial.com'><h3 align="center">PySocial</h3></a>
<p align="center">
    Path to a free self-taught education in <a href='http://python.org'><strong>Python</strong></a> language!
</p>


# PySocial
## Python learning website
Python is an easy to learn language many beginners to coding choose as their first programming language and it is not limited to web development, as you can build games and applications with it. If you are new to programming or simply interested in learning Python, here are some resources you can use.

## Table of contents

* [About](#about)
* [Quick start & Installatoin](#quick-start)


## About
This is a [website](http://pysocial.com) and **solid path** for those of you who want to complete learn **python** language on your own time, **for free**, with contents from the **best refrence** in the World.
This website is an introduction to basic programming concepts and abstractions with series of Python examples to help someone new to Python learn how to program in Python..


## Quick start & Installation

At the first use pip:
-----------
```
pip install -r requirements.txt
```

Make an ini file for settings and then save it into pysocial path:

```
pysocial/settings.ini
```

Fill settings.ini with below options and
Set your customization value for those option's:
-----------
```
[mongodb]
DATABASE_USER: xxxxxxxxxxxx
DATABASE_PASSWORD: xxxxxxxxxxxx
DATABASE_HOST: localhost
DATABASE_PORT: 27017
DATABASE_NAME: PySocial
DATABASE_URL: mongodb://pysocial:27017
DATABASE_LOCAL: mongodb://localhost:27017


[django_db]
DATABASE_USER: xxxxxxxxxxxx
DATABASE_PASSWORD: xxxxxxxxxxxx
DATABASE_HOST: localhost
DATABASE_PORT: 5070
DATABASE_NAME: pysocial


[host]
ON_PYSOCIAL: true
SITE_ID: 1


[secrets]
SECRET_KEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


[debug]
DEBUG: true
TEMPLATE_DEBUG: true
VIEW_TEST: true
INTERNAL_IPS: 127.0.0.1
SKIP_CSRF_MIDDLEWARE: true
DEBUG_TOOLBAR: false


[email]
SERVER_EMAIL: pysocial@localhost
EMAIL_HOST: localhost
MAILGUN_KEY: xxxxxxxxxxxx
MAILGUN_URL: xxxxxxxxxxxx


[logging]
DIR = /var/log/pysocial/
LOG_FORMAT = %(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)s] %(message)s
DATE_FORMAT = %Y-%m-%d %H:%M:%S



[analytic]
TRACK_ID: UA-XXXXXX-1
bing: XXXXXXXXXXXXXXXXXXXXXXXXXXXX
google: XXXXXXXXXXX
alexa: XXXXXXXXXXXXXXXXXXXX

```

Migrate your database for models:
-----------

```
./manage.py migrate
```

Run the collectstatic management command:
-----------
```
./manage.py collectstatic
```

In mongo shell set this indexes:
-----------
```
use PySocial
db.users.createIndex({'username': 1}, {unique: true})
db.acl_group.createIndex({'group_name': 1}, {unique: true})
db.box.createIndex({'title': 1}, {unique: true})
db.settings.createIndex({'parent_name': 1, 'box': 1}, {unique: true, sparse: true})
```



Added group with "Member" name into group user with your permission.

