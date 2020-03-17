from bs4 import BeautifulSoup
from time import sleep
import requests
import pandas as pd

class Amazon:
    """
    This class contains a simple scrape to get
    some data of Amazon website
    """
    def __init__(self, keyword, user):
        self.keyword = keyword
        self.URL = f'https://www.amazon.com/s?k={self.keyword}&ref=nb_sb_noss'
        self.user = user

    def scrap(self):
        page = requests.get(self.URL,
                headers={'user-agent': 'By {self.user}'})
        sleep(2)

        if page.status_code is not 200:
            raise requests.ConnectionError
        else:
            soup = BeautifulSoup(page.text, 'html.parser')
            all_desc = soup.find_all(class_='a-size-medium a-color-base a-text-normal')
            all_prices = soup.find_all(class_='a-offscreen')

            formated_descriptions = [desc.text for desc in all_desc]
            formated_prices = [prices.text for prices in all_prices]

            data_frame = pd.DataFrame(list(zip(formated_descriptions,
                                               formated_prices)),
                                      columns=['Product Description', 'Price']).to_excel(
                'amazon_ws.xlsx',
                engine='xlsxwriter',
                index=False
            )

            return 'Scraping Performed Successfuly'
