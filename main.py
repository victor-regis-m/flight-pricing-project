import scraper
import db_setup
import sys


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session = db_setup.configure()
    s = session()
    s.commit()
    try:
        departure_airport, arrival_airport, departure_date = (sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Missing search query input")
    query = scraper.SearchQuery(departure_airport, arrival_airport, departure_date)
    results = scraper.scrape(query)
    for i in results:
        s.add(i)
    s.commit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
