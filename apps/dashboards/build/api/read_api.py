import requests

def get_api(api = '',token = '', tiempo_espera = 300):
    
    response = requests.get(api, headers={'Authorization': "Bearer {}".format(token)}, timeout=300)

    objeto=response.json()
    list_objetos=objeto['objeto']
    return list_objetos
