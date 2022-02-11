import requests
from flask_babel import _

from app import app


def translate(text, source_lang, dest_lang):
    if (
        'MS_TRANSLATOR_KEY' not in app.config
        or not app.config['MS_TRANSLATOR_KEY']
    ):
        return _('Error! The translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'eastus'
    }
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        + f'/translate?api-version=3.0&from={source_lang}&to={dest_lang}',
        headers=auth,
        json=[{'Text': text}]
    )
    if r.status_code != 200:
        return _('Error! The translation service failed.')
    return r.json()[0]['translations'][0]['text']
