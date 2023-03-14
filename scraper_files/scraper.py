from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from datetime import datetime, timedelta
from database_model import FlightInfo



class SearchQuery:
    best_flight_string = "bestflight_a"
    cheapest_flight_string = "price_a"
    url_base = "https://www.kayak.com.br/flights/"
    def __init__(self, departure_airport, arrival_airport, departure_date):
        self.departure_airport = departure_airport
        self.departure_date = departure_date
        self.arrival_airport = arrival_airport
        self.url_best = \
            f"{SearchQuery.url_base}{departure_airport}-{arrival_airport}/{departure_date}?{SearchQuery.best_flight_string}"
        self.url_cheapest = \
            f"{SearchQuery.url_base}{departure_airport}-{arrival_airport}/{departure_date}?{SearchQuery.cheapest_flight_string}"

    def compile_flight_info(self, info):
        info['departure_airport'] = self.departure_airport
        info['arrival_airport'] = self.arrival_airport
        departure_time = info.pop('time').rjust(5, '0')
        duration = re.findall(r"\d{1,2}(?=h)|\d{2}(?=m)", info['duration'])
        duration_timedelta = timedelta(hours=int(duration[0]), minutes=int(duration[1]))
        departure_datetime = datetime.fromisoformat(f'{self.departure_date}T{departure_time}:00')
        arrival_datetime = departure_datetime + duration_timedelta
        info['stops'] = extract_stop_number(info['stops'])
        info['departure_datetime'] = departure_datetime
        info['arrival_datetime'] = arrival_datetime
        info['query_datetime'] = datetime.fromtimestamp(time.mktime(time.localtime()))
        return info

def extract_stop_number(text):
    m = re.search("\d", text)
    return int(m.group(0)) if m else 0


def scrape(sq):
    driver = setup_webriver()
    driver.get(sq.url_cheapest)
    time.sleep(12)
    offer_texts = select_all_offers(driver)
    clean_info_extracted = [order_flight_info(i) for i in offer_texts]
    flight_info_list = [sq.compile_flight_info(i) for i in clean_info_extracted]
    scraper_output = [convert_to_db_model(flight_info) for flight_info in flight_info_list]
    print("Scraper is done")
    return scraper_output


def setup_webriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver


def select_all_offers(driver):
    wrappers = driver.find_elements(By.XPATH, "//*[contains(@class, 'rapper')]")
    return [wrapper.text for wrapper in wrappers if wrapper_is_offer(wrapper)]


def wrapper_is_offer(wrapper):
    currency_regex = r"R\$"
    return re.search(currency_regex, wrapper.text) and "Ver oferta" in wrapper.text and "Anúncio" not in wrapper.text


def order_flight_info(raw):
    raw = raw.replace('\n', ' ')
    times = re.findall(r"\d{1,2}:\d{2}", raw)
    duration = re.findall(r"\d{1,2}h \d{2}m", raw)
    prices = re.findall(r"(?<=R\$ )(\d{0,3}\.*\d{0,3})", raw)
    stops = re.findall(r"direto|\d escalas*", raw)
    operator = re.findall(r"(?<=\dh \d{2}m).*?(?=R\$)", raw)
    return \
        {
            "time": times[0],
            "duration": duration[0],
            "price": lowest_price(prices),
            "stops": stops[0],
            "operator": operator[0]
        }


def lowest_price(prices):
    return min([clean_price(i) for i in prices])


def clean_price(price):
    return int(price.replace(".", ""))


def convert_to_db_model(flight_info):
    return FlightInfo(
        duration = flight_info["duration"],
        price = flight_info["price"],
        stops = flight_info["stops"],
        operator = flight_info["operator"],
        departure_airport = flight_info["departure_airport"],
        arrival_airport = flight_info["arrival_airport"],
        departure_datetime = flight_info["departure_datetime"],
        arrival_datetime = flight_info["arrival_datetime"],
        query_datetime = flight_info["query_datetime"]
    )
