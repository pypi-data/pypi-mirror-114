from requests import post
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from unicodedata import normalize

API_URL = 'https://www.4devs.com.br/'
PROGRAM = 'ferramentas_online.php'
MATH = 'ferramentas_matematica.php'

HEAD = CaseInsensitiveDict()
HEAD["Content-Type"] = "application/x-www-form-urlencoded"

def htmlForList (html: str, value: str) :
    list = []
    html: BeautifulSoup = BeautifulSoup(html, 'html5lib')
    all_values = html.find_all(value)
    for value in all_values :
        list.append(value.text.strip())
    return list

def htmlForDictionary (html: str, key: str, value: str) :
    dictionary: dict = dict()
    html: BeautifulSoup = BeautifulSoup(html, 'html5lib')
    all_keys = html.select(key)
    all_values = html.select(value)
    for index in range(len(all_keys)) :
        _key = normalize('NFKD', all_keys[index].text).encode('ASCII','ignore').decode('ASCII')
        _value = normalize('NFKD', all_values[index].text).encode('ASCII','ignore').decode('ASCII')
        dictionary[_key] = _value
    return dictionary

def dictionaryForParameters (dictionary: dict) :
    parameters: str = str()
    for key in dictionary : parameters += f'{key}={dictionary.get(key)}&'
    return parameters

def newRequest (type: str, data: dict) :
    parameters = dictionaryForParameters(data)
    if type == 'PROGRAM' : response = post(f'{API_URL}{PROGRAM}', data=parameters, headers=HEAD)
    elif type == 'MATH' : pass
    else : return f'The {type} argument is not valid'
    return response.content.decode('utf-8')