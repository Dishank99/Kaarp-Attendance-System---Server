# from .secrets import *
import requests
import json 

from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

LOCATIONIQ_API_KEY = 'pk.fe79f972a1fb5316b6b3e42607d6ff7d'

def get_location_string(latitude, longitude):
    url = f'https://us1.locationiq.com/v1/reverse.php?key={LOCATIONIQ_API_KEY}&format=json&lat={latitude}&lon={longitude}'
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        print(response.get('display_name'))
    else:
        raise Exception('Not Found')

    return response.get('display_name')
