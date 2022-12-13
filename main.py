import requests
import re 
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from pprint import pprint
import datetime
from exercise_2 import logger


headers = Headers(os='lin', browser="firefox")


@logger('get_html.log')
def get_html(url):

    html = requests.get(url, headers=headers.generate()).text
    
    return html

@logger('pars.log')
def pars(html):
    soup = BeautifulSoup(html, features='lxml')
    results = soup.find_all(class_='serp-item')
    
    for result in results:

        description = result.find(class_="g-user-content")
   
        match = re.search(r'.*Django[\w\d\s\W\S\D]*Flask.*', str(description))
        if match:
            description = result.find(class_="g-user-content").text
        else: 
            continue
        
        city = result.find("div",{"data-qa":"vacancy-serp__vacancy-address"}).text
        campany = result.find(class_="bloko-link bloko-link_kind-tertiary").text

        salary = result.find('span', class_="bloko-header-section-3")
        if salary == None:
            salary = 'Не указана'
        else:
            salary = salary.text

        href = result.find(class_='serp-item__title')['href']
        title = result.find(class_='serp-item__title').text
        
       

        return { 'title': title,
                 'company': campany,
                 'city': city,
                 'slary': salary,
                 'url': href,
                 'description': description }

def create_json(dict): 
    with open("data_file.txt", "w", encoding="utf8") as f:
        json.dump(dict,f, ensure_ascii=False, indent=4)


def main():
    data = {}
    data['vacancy'] = []
    for i in range(50):
        url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page="+str(i)+"&hhtmFrom=vacancy_search_list"
    
        body =  pars(get_html(url))

        print(f'{i*2}%',end='')
        if body != None:
            data['vacancy'].append(body)
            print('+') 
        else: print()
            

    create_json(data)
    print('Файл успешно создан')


if __name__ == '__main__':
    main() 