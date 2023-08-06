import requests
import json
import pandas as pd

class World2Vec:
    def __init__(self, API_KEY):
        self.API_URL = 'https://api.world2vec.com'
        self.API_KEY = API_KEY

    def get_by_id(self, ids, start=None, end=None):
        params = {
            'series': ids,
            'api_key': self.API_KEY,
            'type': 'dataframe-skinny'
        }
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        response = requests.post(f'{self.API_URL}/numbers', json=params)
        loaded = json.loads(response.content)
        df = pd.DataFrame(loaded['data'], columns=loaded['columns'])
        df['time'] = df['time'].astype('datetime64[ms]')
        return df
  
    def get_by_query(self, query, start=None, end=None):
        time_params = '&start=' + start if start else '' + '&end=' + end if end else ''
        url = f'{self.API_URL}/numbers/query/${query}?type=dataframe-skinny'
        if len(time_params) > 0:
            url += time_params
        response = requests.get(url)
        loaded = json.loads(response.content)
        df = pd.DataFrame(loaded['data'], columns=loaded['columns'])
        df['time'] = df['time'].astype('datetime64[ms]')
        return df
