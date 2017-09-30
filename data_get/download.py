import os
import csv
import requests

from bs4 import BeautifulSoup


dir_path = os.path.dirname(os.path.realpath(__file__))
save_dir = os.path.join(dir_path, '..', 'data_source')

header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:32.0) Gecko/20100101 Firefox/51.0',}

def download():
    urls = {'reddit_archive': 'https://docs.google.com/spreadsheets/d/1X1HTxkI6SqsdpNSkSSivMzpxNT-oeTbjFFDdEkXD30o/export?format=csv&id=1X1HTxkI6SqsdpNSkSSivMzpxNT-oeTbjFFDdEkXD30o&gid=695409533',
            'va_prices': 'https://www.abc.virginia.gov/library/products/other-documents/price-list-excel.csv?la=en'
           }
    for name, url in urls.items():
        file_path = os.path.join(save_dir, '{}.csv'.format(name))
        with open(file_path, 'wb') as handle:
            response = requests.get(url, stream=True, headers=header)
            if response.ok:
                for block in response.iter_content(1024):
                    handle.write(block)


def scrape_proof66():
    urls = ['http://www.proof66.com/liquor/american-whiskey.html',
            'http://www.proof66.com/liquor/canadian-whisky.html',
            'http://www.proof66.com/liquor/irish-whiskey.html',
            'http://www.proof66.com/liquor/international-whisky.html',
            'http://www.proof66.com/liquor/scotch-whisky.html']

    final_rows = []
    for url in urls:
        r = requests.get(url,  headers=header)
        soup = BeautifulSoup(r.text, 'html5lib')
        category_grid = soup.find_all("section", {"id": "categorygrid"})
        section = category_grid[0].select("div[class=row]")
        headers = ["Name", "Rating", "Rabble", "Price"]
        for s in range(len(section)):
            cells = section[s].find_all("span", {"class": "font14s480"})
            name = cells[0].get_text()
            rating = cells[1].get_text()
            rabble = cells[2].get_text()
            price = cells[3].get_text()
            final_rows.append([name, rating, rabble, price])

    file_path = os.path.join(save_dir, 'proof66.csv')
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in final_rows:
            writer.writerow(row)


def scrape_metacritic():
    urls = ['http://whiskyanalysis.com/index.php/database/']
    r = requests.get(urls[0], headers=header)

    soup = BeautifulSoup(r.text, 'html5lib')

    table = soup.find_all("table", {"class": "igsv-table"})
    th = table[0].select("th")

    final_rows = []
    final_headings = []
    for cell in th:
        final_headings.append(cell.get_text().lower().replace(' ', '_').replace('#', 'count'))

    final_rows.append(final_headings)

    rows = table[0].find_all('tbody')[0].find_all('tr')
    for row in rows:
        td = row.select('td')
        cells = []
        for cell in td:
            cells.append(cell.get_text().encode('ascii', 'ignore').decode('ascii'))
        final_rows.append(cells)

    file_path = os.path.join(save_dir, 'metacritic.csv')
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for row in final_rows:
            writer.writerow(row)


if __name__ == '__main__':

    download()
    scrape_proof66()
    scrape_metacritic()
