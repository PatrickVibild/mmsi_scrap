import requests
from bs4 import BeautifulSoup

from mmsi_data import ShipData
from mongo_repo import AISMongo


def scrap_mmsi_data(mmsi):
    def get_vessel_type(s):
        generic = s.find('h2', class_='vst').text
        meta = generic.split(',')
        return meta[0]

    def get_built_year(s):
        try:
            year = s.find_all('section', class_='ship-section')[3].find('div').find('div').find('table').find('tbody').find_all('tr')[10].find('td', class_='v3').text
        except:
            year = None
        return year

    def get_dimension(s):
        try:
            l = s.find('table', class_='aparams').find('tbody').find_all('tr')[9].find('td', class_='v3').text
            l = l.replace('m', '')
            l = l.replace(' ', '')
            dim = l.split('/')
            length = dim[0]
            beam = dim[1]
        except:
            length = None
            beam = None
        return length, beam

    def get_gross_tonnage(s):
        try:
            gt = s.find_all('section', class_='ship-section')[3].find('div').find('div').find('table').find('tbody').find_all('tr')[5].find('td', class_='v3').text
        except:
            gt = None
        return gt

    id = str(mmsi)
    URL = 'https://www.vesselfinder.com/vessels/details/' + mmsi
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, "html.parser")

    g = get_vessel_type(soup)
    year = get_built_year(soup)
    l, b = get_dimension(soup)
    t = get_gross_tonnage(soup)
    return ShipData(id, g, year, l, b, t)


class MMSIWizard:
    def __init__(self):
        self.mmsi_db = AISMongo()

    def get_mmsi(self, mmsi):
        if self.mmsi_db.exist_mmsi(mmsi):
            print('DB-ed')
            return self.mmsi_db.get_mmsi(mmsi)
        mmsi_data = scrap_mmsi_data(mmsi)
        self.mmsi_db.insert_mssi(mmsi_data)
        print('Scrap-ed')
        return mmsi_data

if __name__ == '__main__':
    little_wizzard = MMSIWizard()
    info = little_wizzard.get_mmsi('440055170')
    print(info.to_dict())

    del little_wizzard

