import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = 'http://www.parliament.go.ke'


def get_all_mps(pg):
    MPS_URL = f'{BASE_URL}/the-national-assembly/mps?field_name_value=%20&field_parliament_value=2017&page={pg}'
    PAGE = requests.get(MPS_URL)
    soup = BeautifulSoup(PAGE.content, 'html.parser')
    results = soup.find_all('tr', class_='mp')
    with open(f'mps{pg}.csv', mode='w') as csv_file:
        fieldnames = ['name', 'img_url', 'county', 'constituency', 'party', 'field_status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in results:
            writer.writerow({
                'name': i.find('td', class_='views-field-field-name').text.strip(),
                'img_url': get_better_image(
                    f"{BASE_URL}{i.find('td', class_='views-field-view-node').find('a').get('href')}"),
                'county': i.find('td', class_='views-field-field-county').text.strip(),
                'constituency': i.find('td', class_='views-field-field-constituency').text.strip(),
                'party': i.find('td', class_='views-field-field-party').text.strip(),
                'field_status': i.find('td', class_='views-field-field-status').text.strip()
            })


def get_better_image(url):
    PAGE = requests.get(url)
    soup = BeautifulSoup(PAGE.content, 'html.parser')
    results = soup.find_all('div', class_='profile-pic')
    return f"{BASE_URL}{results[0].find('img')['src']}"


def get_all_senators(pg):
    SENATORS_URL = f'{BASE_URL}/the-senate/senators?title=&field_parliament_value=2017&page={pg}'
    PAGE = requests.get(SENATORS_URL)
    soup = BeautifulSoup(PAGE.content, 'html.parser')
    results = soup.find_all('tr')
    with open(f'senators{pg}.csv', mode='w') as csv_file:
        fieldnames = ['name', 'img_url', 'county', 'party', 'field_status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in results:
            if i.find('td') is None:
                continue
            print(f"Writing to senators{pg}")
            writer.writerow({
                'name': i.find('td', class_='views-field-field-senator').text.strip(),
                'img_url': get_better_image(
                    f"{BASE_URL}{i.find('td', class_='views-field-view-node').find('a').get('href')}"),
                'county': i.find('td', class_='views-field-field-county-senator').text.strip(),
                'party': i.find('td', class_='views-field-field-party-senator').text.strip(),
                'field_status': i.find('td', class_='views-field-field-status-senator').text.strip()
            })


if __name__ == '__main__':
    for i in range(0, 7):
        get_all_senators(i)
    for i in range(0, 37):
        get_all_mps(i)
