import pytest


@pytest.fixture(scope="session")
def scrape_craigslist():
    from scraper import fetch_search_results
    body, encoding = fetch_search_results('Near downtown seattle', 1500,2500,2)

    return body, encoding


def test_fetch(scrape_craigslist):
    from scraper import read_search_results

    body, encoding1 = scrape_craigslist
    apartment, encoding2 = read_search_results()
    assert apartment == body
    assert encoding1 == encoding2


def test_extract_listing(scrape_craigslist):
    from scraper import parse_source, extract_listings, read_search_results

    body, encoding = scrape_craigslist
    parsed_body = parse_source(body, encoding)

    extracted = extract_listings(parsed_body)

    apartment = parse_source(read_search_results()[0], encoding)
    apartment2 = extract_listings(apartment)

    assert extracted == apartment2



