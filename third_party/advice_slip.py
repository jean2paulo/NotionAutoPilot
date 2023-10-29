import requests

def get_random_quote():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    advice = response.json()["slip"]["advice"]

    return advice