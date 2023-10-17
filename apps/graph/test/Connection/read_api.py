import pandas as pd
import numpy as np
import requests

def getApi(api,token):
    response = requests.get(api, headers={'Authorization': "Bearer {}".format(token)})
    objeto=response.json()
    list_objetos=objeto['objeto']
    return list_objetos
