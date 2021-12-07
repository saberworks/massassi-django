# massassi-django

The Massassi Temple dynamic backend

This is a python/django project that replaces decades-old php3/4/5 code on [The Massassi Temple](https://www.massassi.net/), a Dark Forces II: Jedi Knight fan site that's been active since 1998.

## Prerequisites

* python 3
* postgresql server (you can see how I do it if you check out the [massassi.net repo](https://github.com/saberworks/massassi.net) and look at the docker-compose.yml file)
* I've only ever run this on linux but I suppose it will work on mac & windows with the correct setup

## Instructions

To get it up and running (these were from memory so hopefully they work):

* Clone the repo and `cd` into the `massassi-django` directory
* Create a virutal environment so you can install dependencies without interfering with your system python: `python3 -m venv ./env`
* Activate your virtual environment: `source env/bin/activate`
* Now when you use `python` from the command line in a terminal that has been "activated", it will use your virtual environment's python and you can safely install modules without interfering with any other project
* Install the python dependencies: `pip install -r requirements.txt`
* Modify the config file(s) in `massassi/settings/` (don't forget to specify database connection info)
* Initialize the database schema:
    * `python manage.py makemigrations`
    * `python manage.py migrate`
* run the dev server: `python manage.py runserver`

Probably the whole thing will look broken because most of the static stuff is missing.  That stuff is in a separate repo [massassi-static](https://github.com/saberworks/massassi-static), but if you want everything to work you might want to try running the whole system [massassi.net](https://github.com/saberworks/massassi.net).
