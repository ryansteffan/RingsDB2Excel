import requests


def get_packs():
    request_output = requests.get("https://ringsdb.com/api/public/packs/", {})
    return request_output.json()


print(get_packs())
