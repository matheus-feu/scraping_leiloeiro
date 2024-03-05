from typing import Any

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class AuctionDataExtractor:
    def __init__(self, driver):
        self.driver = driver

    def extract_location(self) -> dict:
        try:
            location_element = self.driver.find_element(
                By.XPATH, '//div[@class="locality item"]/div[@class="value"]').text.split(',')
        except NoSuchElementException:
            location_element = None

        return {
            'address': location_element[0].strip(),
            'number': location_element[1].strip(),
            'neighborhood': location_element[2].strip(),
            'city': location_element[3].strip(),
            'state': location_element[4].strip(),
        }

    def get_title(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/div/h1').text
        except NoSuchElementException:
            return None

    def get_process_number(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[3]/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/a').text
        except NoSuchElementException:
            return None

    def get_first_auction(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[3]/div[2]/div[3]/div[2]/div[2]/span[1]').text
        except NoSuchElementException:
            return None

    def get_first_auction_price(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[3]/div[2]/div[3]/div[2]/div[2]/span[3]').text
        except NoSuchElementException:
            return None

    def get_second_auction(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[3]/div[2]/div[3]/div[2]/div[3]/span[1]').text
        except NoSuchElementException:
            return None

    def get_second_auction_price(self):
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[3]/div[2]/div[3]/div[2]/div[3]/span[3]').text
        except NoSuchElementException:
            return None

    def get_auctioneer(self):
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div[2]').text
        except NoSuchElementException:
            return None

    def get_description(self) -> Any | None:
        try:
            description_elements = self.driver.find_elements(By.XPATH,
                                                             '//div[@class="col-sm-6 col-md-8 description border"]/div')
            description_texts = [element.text for element in description_elements]
            return ' '.join(description_texts)
        except NoSuchElementException:
            return None

    def get_author(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[3]/div[2]/div[2]/div/div/div[2]/div[3]/div[2]').text
        except NoSuchElementException:
            return None

    def get_img(self) -> Any | None:
        try:
            return self.driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[1]/div[1]/div/div[3]/div/img').get_attribute('src')
        except NoSuchElementException:
            return None
