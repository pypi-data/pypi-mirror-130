import requests
import json
import pandas as pd

class World2Vec:
    def __init__(self, API_KEY):
        self.API_URL = 'https://api.world2vec.com'
        self.API_KEY = API_KEY

    def get_by_id(self, ids):
        params = {
            'series': ids,
            'api_key': self.API_KEY,
            'type': 'dataframe-skinny'
        }
        response = requests.post(f'{self.API_URL}/numbers', json=params)
        loaded = json.loads(response.content)
        df = pd.DataFrame(loaded['data'], columns=loaded['columns'])
        df['time'] = df['time'].astype('datetime64[ms]')
        return df
  
    def get_by_query(self, query):
        response = requests.get(f'{self.API_URL}/numbers/query/${query}?type=dataframe-skinny')
        loaded = json.loads(response.content)
        df = pd.DataFrame(loaded['data'], columns=loaded['columns'])
        df['time'] = df['time'].astype('datetime64[ms]')
        return df
