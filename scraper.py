import requests
from bs4 import BeautifulSoup
import sys


def fetch_search_results(
    query=None, minAsk=None, maxAsk=None, bedrooms=None
):
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()

    with open('apartments.html', 'w') as the_file:
        the_file.write(resp.content)

    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed


def extract_listings(parsed):
    location_attrs = {'data-latitude': True, 'data-longitude' : True}
    listings = parsed.find_all('p', class_='row')
    extracted = []
    for listing in listings:
        location = {key: listing.attrs.get(key, '') for key in location_attrs}
        link = listing.find('span', class_='pl').find('a')
        price_span = listing.find('span', class_='price')
        this_listing = {'location':location, 'link': link.attrs['href'],
                                        'description': link.string.strip(),
                                        'price': price_span.string.strip(),
                                        'size': price_span.next_sibling.strip(' \n-/')}
        extracted.append(this_listing)
    return extracted


def read_search_results():
    with open('apartments.html', 'r') as the_file:
        file_ = the_file.read()

    return file_, 'utf-8' #find how to extract encoding from file read.

if __name__ == '__main__':
    import pprint
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(minAsk=500, maxAsk=1000, bedrooms=2)

    doc = parse_source(html, encoding)
    listings = extract_listings(doc)
    print len(listings)
    pprint.pprint(listings[0])

