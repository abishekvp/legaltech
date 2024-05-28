from googlesearch import search
from bs4 import BeautifulSoup
import requests

def google_search(query):
    results = search(query)
    for result in results:
        response = requests.get(result)
        soup = BeautifulSoup(response.content, 'html.parser')
        answer = soup.find('div', class_='kno-rdesc')
        if answer:
            return answer.text
response = google_search("Was ist die Hauptstadt von Deutschland")
print(response)
