#!/user/bin/python
import requests
import re
from bs4 import BeautifulSoup

# URL = 'https://www.serebii.net/pokedex-swsh/bulbasaur/'
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')

def get_name(soup):
    name = ""
    title = soup.find('title')
    title_str = str(title.string)
    index = title_str.rfind('#')
    if index > -1:
        name = title_str[0:index-3]
    return name.lower()

def get_types(soup):
    types = []
    for img in soup.find_all('img', class_='typeimg'):
        types.append(img['alt'])
    return types
def parse_number(s):
    s = s[2:5]
    return int(s)

def get_number(soup):
    headers = soup.find_all('h1')
    for header in headers:
        matches = header.find_all(string=re.compile('#'))
        for match in matches:
            s = str(match.string)
            s = parse_number(s)
            return s
def get_stats(soup):
    stats = {}
    stat_map = {
        0: "total",
        1: "hp",
        2: "attack",
        3: "defense",
        4: "special attack",
        5: "special defense",
        6: "speed",
    }
    for section in soup.find_all('a'):
        if section.get('name') == 'stats':
            stat_table = section.findNext('table')
            current_row = 0
            for row in stat_table.contents:
                if current_row == 3:
                    current_cell = 0
                    for cell in row.contents:
                        if current_cell % 2 == 0:
                            index = current_cell/2
                            data = cell.getText()
                            if index == 0:
                                arr = [int(s) for s in data.split() if s.isdigit()] #parse base stats
                                data = arr[0]
                            else:
                                data = int(data)
                            stats[stat_map[index]] = data
                        # print(current_cell, type(cell), cell)
                        current_cell += 1
                current_row += 1        
    return stats

def get_next_url(soup):
    url = ''
    links = soup.find_all('a')
    for link in links:
        instances = link.find_all(string=re.compile("#"))
        for instance in instances:
            parent = instance.parent
            url = parent['href']        
    return url

def get_data(count,soup):
    baseURL = 'https://www.serebii.net'       
    get_next_url(soup)
    pokemon_names = []
    pokemon_data = []
    for num in range(count):
        name = get_name(soup)
        types = get_types(soup)
        stats = get_stats(soup)
        number = get_number(soup)
        next_url = baseURL + get_next_url(soup)
        current = {
            'number':number,
            'name':name,
            'types':types,
            'stats':stats,
        }
        pokemon_data.append(current)
        pokemon_names.append(name)
        next_page = requests.get(next_url)
        soup = BeautifulSoup(next_page.content, 'html.parser')
        ret = [pokemon_data, pokemon_names]
    return ret
def scrape_pokemon(count):
    URL = 'https://www.serebii.net/pokedex-swsh/bulbasaur/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    data_arr = get_data(count,soup)
    # pokemon_list = data_arr[1]
    # data = data_arr[0]
    return data_arr
