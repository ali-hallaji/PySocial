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

Migrate your database for models:
-----------

```
./manage.py migrate
```

Added group with "Member" name into group user with your permission.

In mongo shell set this indexes:
-----------
```
use PySocial
db.users.createIndex({'username': 1}, {unique: true})
```
