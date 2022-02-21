# Microblog

## Description

App allows to create text posts for logged in users, to follow & unfollow other users, to translate posts written in different languages, supports localization for 🇷🇺, 🇬🇧 & 🇫🇮.

## Technology Stack

[![Python](https://img.shields.io/badge/-Python-464646??style=flat-square&logo=Python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/-Flask-464646??style=flat-square&logo=Flask)](https://flask.palletsprojects.com/en/2.0.x/)
[![SQL%20Alchemy](https://img.shields.io/badge/-SQL%20Alchemy-464646??style=flat-square&logo=sqlite)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/-Bootstrap-464646??style=flat-square&logo=Bootstrap)](https://getbootstrap.com/)
[![Babel](https://img.shields.io/badge/-Babel-464646??style=flat-square&logo=Babel)](https://babel.pocoo.org/en/latest/)
[![Azure%20Translator](https://img.shields.io/badge/-Azure%20Translator-464646??style=flat-square&logo=microsoftazure)](https://azure.microsoft.com/en-us/services/cognitive-services/translator/)
[![MomentJS](https://img.shields.io/badge/-MomentJS-464646??style=flat-square&logo=javascript)](https://momentjs.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-464646??style=flat-square&logo=heroku)](https://www.heroku.com/)
[![Docker](https://img.shields.io/badge/-Docker-464646??style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/-Redis-464646??style=flat-square&logo=redis)](https://redis.io/)

- Python
- Flask
- SQL Alchemy
- Bootstrap
- Babel
- Azure Translator
- MomentJS
- Elasticsearch
- Heroku
- Docker
- Redis

## Deployment

Clone the repo and change directory to the cloned repo:

```bash
git clone https://github.com/hardkoro/flask_microblog.git
```

```bash
cd flask_microblog
```

Create and activate virtual environment:

```bash
python3 -m venv venv
```

```bash
. venv/bin/activate
```

Install requirements from file requirements.txt:

```bash
pip3 install -r requirements.txt
```

Provide flask environmen data via ```.flaskenv```:

```bash
touch .flaskenv
cat >> .flaskenv

FLASK_APP=microblog.py  # name of the flask app
FLASK_ENV=production    # stage (e.g. 'production', 'development')
```

Provide sensitive data via ```.env``` file:

```bash
touch .env
cat >> .env

SECRET_KEY=paste_your_secret_key      # app's secret key
DATABASE_URL=paste_your_database_url  # database URL

MAIL_SERVER=paste_your_mail_server_host   # mail server host
MAIL_PORT=paste_your_mail_server_port     # mail server port
MAIL_USERNAME=paste_your_mail_username    # mail username
MAIL_PASSWORD=paste_your_mail_password    # mail password
MAIL_USE_TLS=paste_1_if_your_mail_server_uses_tls   # enable TLS

MS_TRANSLATOR_KEY=paste_your_key                  # Microsoft Azure Translator key
MS_TRANSLATOR_REGION_NAME=paste_your_region_name  # Microsoft Azure Translator region name

ELASTICSEARCH_URL=paste_your_elasticsearch_url    # Elasticsearch URL
REDIS_URL=paste_your_redis_url                    # Redis URL

LOG_TO_STDOUT=1   # specifies logging to stdout (e.g. for Heroku)
```

To emulate a mail server one might use another terminal window with the following command:

```bash
python -m smtpd -n -c DebuggingServer localhost:8025
```

Run app:

```bash
flask run
```

## Information

Application based on [Miguel Grinberg's tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) on Flask web application

## Translations

To provide more simpler way to add new translations one can use such commands:

* to add a new language: 
  ```bash
  flask translate init LANG 
  ```
  
* to update all language repositories: 
  ```bash
  flask translate update  
  ```
  
* to compile all language repositories: 
  ```bash
  flask translate compile 
  ```

Translations are kept at: ```/app/translations``` folder.

## Microsoft Translator API

To setup Microsoft Azure Translator, login to your Azure account, go to the Azure Portal & clcick on the "Create a resource" button. Find "Translator", select it & clieck the "Create" button.

Fill the form as follows:
```
Subscription: Pay-As-You-Go
Resource group: (New) your-microblog-resource-group-name
Resource group region: your-resource-group-region
Resource region: your-resource_region
Name: your-resource-name
Pricing tier: Free F0 (Up to 2M characters translated)
```

Click the "Review + create" button & then "Create", the translator API resource will be added to your account.

To obtain the key click the "Go to resource" button & then find the "Keys and Endpoint" option on the left sidebar. Copy one of the keys & the name of the region to your ```.env``` file as ```MS_TRANSLATOR_KEY``` and ```MS_TRANSLATOR_REGION_NAME``` respectively. 

## Elasticsearch

Setup the latest Elasticsearch version following the steps as described at Elasticsearch site:
https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html

Add Elasticsearch URL to your ```.env``` file as ```ELASTICSEARCH_URL```. Search engine may be switched to another technology by updating ```app/search.py``` module. The model may be included in search engine by providing inheritance from ```SearchableMixin``` mixin.

If the search is being added to the service with some existing posts, then posts should have to be indexed as follows:

```bash
flask shell

from app.search import add_to_index
from post in Post.query.all():
	add_to_index('post', post)
```

## Heroku Deployment

Login to Heroku via Heroku CLI:

```bash
heroku login
```

Create an application:

```bash
heroku apps:create hk-flask-microblog
```

Add Heroku Postgres database:

```bash
heroku addons:add heroku-postgresql:hobby-dev
```

As Heroku requires logs to be outputted to ```stdout``` set an environment variable ```LOG_TO_STDOUT```:

```bash
heroku config:set LOG_TO_STDOUT=`
```

Add Elasticsearch hosting via SearchBox add-on & Heroku Redis add-on:

```bash
heroku addons:create searchbox:starter
heroku addons:create heroku-redis:hobby-dev
```

Get ```SEARCHBOX_URL``` environment variable from Elasticsearch service & set the correspondent ```ELASTICSEARCH_URL``` variable*:

```bash
heroku config:get SEARCHBOX_URL
heroku config:set ELASTICSEARCH_URL=<your-elastic-search-url>
```

*don't forget to add port to the URL as the setup requires scheme, host & port (443 by default for SSH)

```REDIS_URL``` is going to be added to your Heroku environment automatically.

Open SearchBox Elasticsearch resource panel and manually create an index for Post model via Dashboard > Indices > New index.

Set remaining ```.env``` & ```.flaskenv``` variables as follows:

```bash
heroku config:set ENV_VAR_NAME=env_var_value
```

Start the deployment:

```bash
git push heroku master
```

The corresponding Procfile should contain one web dyno & one worker:

```Procfile
web: flask db upgrade; flask translate compile; gunicorn microblog:app
worker: rq worker -u $REDIS_URL microblog-tasks
```

After deploying, one can start the worker with the following command:

```bash
heroku ps:scale worker=1
```

## Docker Deployment

Install Docker & Docker-compose:

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Create ```.env``` file & fill it with environment variables as follows (assuming PostgreSQL usage):

```bash
touch .env
cat >> .env

SECRET_KEY=paste_your_secret_key      # app's secret key
DATABASE_URL=postgresql://postgres_user:postgres_pwd@db/postgres_db   # Postgres DB URL (container db)
POSTGRES_USER=postgres_user     # Postgres user
POSTGRES_PASSWORD=postgres_pws  # Postgres password
POSTGRES_DB=postgres_db         # Postgres database name

MAIL_SERVER=paste_your_mail_server_host   # mail server host
MAIL_PORT=paste_your_mail_server_port     # mail server port
MAIL_USERNAME=paste_your_mail_username    # mail username
MAIL_PASSWORD=paste_your_mail_password    # mail password
MAIL_USE_TLS=paste_1_if_your_mail_server_uses_tls   # enable TLS

MS_TRANSLATOR_KEY=paste_your_key                  # Microsoft Azure Translator key
MS_TRANSLATOR_REGION_NAME=paste_your_region_name  # Microsoft Azure Translator region name

ELASTICSEARCH_URL=http://es:9200    # Elasticsearch URL (container es)
REDIS_URL=redis::/redis:6379        # Redis URL (container redis)
```

Run containers:

```bash
docker-compose up -d
```

The service will be running at http://localhost:8000/

## Configuring Redis

Install Redis:

```bash
sudo apt update
sudo apt install redis-server
```

Change ```supervised``` directive to ```systemd``` to install Redis as a service in Ubuntu:

```bash
sudo nano /etc/redis/redis.conf
```

Restart service:

```bash
sudo systemctl restart redis.service
```

Test service:

```bash
sudo systemctl status redis
```

The output should contain words like ```active``` / ```running``` / ```enabled```.