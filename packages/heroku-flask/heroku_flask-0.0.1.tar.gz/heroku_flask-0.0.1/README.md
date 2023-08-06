# Heroku Flask Setup

## Run & setup 

### Linux

`$ heroku_flask.sh`

### Windows

`$ heroku_flask.bat`


## Creating List Of Files

* Procfile
* runtime.txt
* app.py
* wsgi.py


### Procfile


```
web: gunicorn wsgi:app
```

### runtime.txt

```
python-3.6.9
```


### app.py

```
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to HK World</h1>"

```

### wsgi.py

```
from app import app

if __name__ == "__main__":
    app.run()

```

## Extra Information

### Create Heroku App

Login to heroku CLI using 

`$ heroku login`

Now, Create a unique name for your Web app.

`$ heroku create heroku-flask-app`

Push your code from local to the heroku remote

`$ git push heroku master`
