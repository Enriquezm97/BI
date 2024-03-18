import requests

def status_cliente(ip = ""):
    try:
        if ip == None:
            return False
        else:
            response = requests.get(f"http://{ip}:3005/")
            if response.status_code == 200:
                return True
            else:
                return False
    except:
        return False