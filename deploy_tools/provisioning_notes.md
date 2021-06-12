Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.9
* virtualenv
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python3.9 python3-venv

##  Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.de

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., staging.my-domain.de

## Folder Structure

Assume we have a user account at /home/username

/home/username
    sites
        DOMAIN1
            .env
            db.sqlite3
            manage.py etc
            static
            virtualenv
        DOMAIN2
            .env
            db.sqlite3
            etc
