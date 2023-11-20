import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
date_now = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
file_path = f"alimentos_{date_now}.txt"
valores_principais = []

url_base = 'http://www.tbca.net.br/base-dados/composicao_alimentos.php'

aliment_codes = []

params = {'pagina': 1}

cod_request_loop = True

while cod_request_loop:
    response = requests.get(url_base, params=params)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        tbody_element = soup.find('tbody')
        if tbody_element:
            tr_elements = tbody_element.find_all('tr')
            if tr_elements:
                for tr in tr_elements:
                    td_1 = tr.find_all('td')[0].text.strip()
                    td_5 = tr.find_all('td')[4].text.strip()
                    aliment_codes.append((td_1, td_5))
            else:
                cod_request_loop = False
        else:
            cod_request_loop = False
        params['pagina'] += 1
    else:
        cod_request_loop = False
aliment_codes = list(set(aliment_codes))

result = []

for cod, aliment_class in aliment_codes:
    print('scrapping ->', cod)
    url = f'http://www.tbca.net.br/base-dados/int_composicao_alimentos.php?cod_produto={cod}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    description_element = soup.find('h5', {'id': 'overview'})
    description = description_element.text.split('Descrição:')[1].split('<<')[0].strip()
    table = soup.find('table')
    thead = table.find('thead')
    headers = thead.find_all('th')[:3]
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    nutrients = []

    for row in rows:
        values = row.find_all('td')[:3]
        row_data = {}
        for i, header in enumerate(headers):
            row_data[header.text.strip()] = values[i].text.strip()
        nutrients.append(row_data)

    alimento_json = {
        'codigo': cod,
        'classe': aliment_class,
        'descricao': description,
        'nutrientes': nutrients
    }

    with open(file_path, "a",encoding='utf-8') as file:
        json_str = json.dumps(alimento_json,ensure_ascii=False)
        file.write(json_str + "\n")

