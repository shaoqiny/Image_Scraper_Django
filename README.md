# Image_Scraper_Django
Web Application that scrapes pictures from url

## How to start

### Run image scraper local

Please make sure you have following dependencies installed:

1. venv
2. pip

### Instructions

Create a virtual environment and install all packages in requirements.txt:
```sh
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip3 install -r requirements.txt
```

Then run following code to start image scraper：

```sh
    $ python3 manage.py runserver
```

Then you should be able to see the image scraper on http://127.0.0.1:8000/

### Account & password

Image scraper requires log in to use, use the following accounts to do the search:

```
# Admin account
username:admin
password:admin123456

# User account
username:user1
password:thisisuser1
```
