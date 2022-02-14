# Microblog

## Description

App allows to create text posts for logged in users, to follow & unfollow other users, to translate posts written in different languages, supports localization for 🇷🇺, 🇬🇧 & 🇫🇮.

## Technology Stack

[![Python](https://img.shields.io/badge/-Python-464646??style=flat-square&logo=Python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/-Flask-464646??style=flat-square&logo=Flask)](https://flask.palletsprojects.com/en/2.0.x/)
[![SQL%20Alchemy](https://img.shields.io/badge/-SQL%20Alchemy-464646??style=flat-square&logo=SQL%20Alchemy)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/-Bootstrap-464646??style=flat-square&logo=Bootstrap)](https://getbootstrap.com/)
[![Babel](https://img.shields.io/badge/-Babel-464646??style=flat-square&logo=Babel)](https://babel.pocoo.org/en/latest/)
[![Azure%20Translator](https://img.shields.io/badge/-Azure%20Translator-464646??style=flat-square&logo=Azure)](https://azure.microsoft.com/en-us/services/cognitive-services/translator/)
[![MomentJS](https://img.shields.io/badge/-MomentJS-464646??style=flat-square&logo=MomentJS)](https://momentjs.com/)

- Python
- Flask
- SQL Alchemy
- Bootstrap
- Babel
- Azure Translator
- MomentJS
- Elasticsearch

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

MAIL_SERVER=localhost   # mail server host
MAIL_PORT=8025          # mail server port

MS_TRANSLATOR_KEY=paste_your_key                  # Microsoft Azure Translator key
MS_TRANSLATOR_REGION_NAME=paste_your_region_name  # Microsoft Azure Translator region name

ELASTICSEARCH_URL=paste_your_elasticsearch_url    # Elasticsearch URL
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

## To-Do List

* 404 on ```/``` page
* Check Translator
