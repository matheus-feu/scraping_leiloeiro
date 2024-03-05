import re

from loguru import logger
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

from app.services.extractor_service import AuctionDataExtractor
from app.services.selenium_setup import SetupDriver


class ScrapingService(SetupDriver):
    def __init__(self,
                 state: str,
                 order_by: str = 'padrao',
                 headless: bool = True,
                 selenoid: bool = False,
                 host: str = 'localhost'):

        super().__init__(url=f"https://www.megaleiloes.com.br/imoveis/{state}", selenoid=selenoid, headless=headless)
        self.driver = self.setup(host=host, name='scraping_bot')
        self.extractor = AuctionDataExtractor(self.driver)
        self.state = state
        self.order_by = order_by
        self.auctions: list[dict] = []
        self.hrefs: list[str] = []
        self.start_driver()

    def accept_cookies(self):
        try:
            self.driver.find_element(By.ID, 'adopt-accept-all-button').click()
        except NoSuchElementException:
            pass

    def ordering_page(self) -> str:
        """
        Ordering page by order_by, 'padrao' is the default, but you can use 'menor_preco', 'maior_preco' or 'popularidade'
        :param order_by: str - default is 'padrao'
        """
        if self.order_by != 'padrao':
            self.driver.find_element(By.ID, 'w1').click()
            self.driver.find_element(By.XPATH, f'//a[@data-sort="{self.order_by}"]').click()
        return self.order_by

    def verify_qtd_pages(self) -> int:
        match = re.search(
            pattern=r'Página \b\d+\b de \b(\d+)\b',
            string=self.driver.find_element(By.XPATH, '//div[@class="summary"]').text
        )
        if match:
            logger.info(f"Total pages: {match.group(1)}")
            return int(match.group(1))
        return 0

    def get_auctions(self) -> list[dict]:
        total_pages = self.verify_qtd_pages()
        order_by = self.ordering_page()

        for page in range(1, total_pages + 1):
            try:
                self.driver.get(f'https://www.megaleiloes.com.br/imoveis/{self.state}?ordem={order_by}&pagina={page}')
                logger.info(f"Scraping page {page}...")
            except WebDriverException as e:
                logger.error(f"Error: {e}")
                break

            elements = self.driver.find_elements(By.XPATH,
                                                 '//*[@id="w0"]/div[1]/div[@class="col-sm-6 col-md-4 col-lg-3"]')

            for element in elements:
                try:
                    href = element.find_element(By.XPATH, './/a[@class="card-image lazyloaded"]').get_attribute('href')
                    if href:
                        self.driver.get(href)
                        auction = {
                            'title': self.extractor.get_title(),
                            'process': self.extractor.get_process_number(),
                            'location': self.extractor.extract_location(),
                            'link': href,
                            'first_auction': self.extractor.get_first_auction(),
                            'first_auction_price': self.extractor.get_first_auction_price(),
                            'second_auction': self.extractor.get_second_auction(),
                            'second_auction_price': self.extractor.get_second_auction_price(),
                            'auctioneer': self.extractor.get_auctioneer(),
                            'description': self.extractor.get_description(),
                            'author': self.extractor.get_author(),
                            'img': self.extractor.get_img()
                        }
                        self.auctions.append(auction)
                        logger.info(f"Auction: {self.auctions}")
                        self.driver.back()
                except NoSuchElementException:
                    continue

        return self.auctions

    def run(self) -> list[dict] | Exception:
        """
        Run the scraping service
        """
        try:
            logger.info(f"Scraping auctions from {self.state}...")
            self.accept_cookies()
            logger.info(f"Verifying quantity of pages and ordering by {self.order_by}...")
            return self.get_auctions()
        except Exception as e:
            logger.error(f"Error: {e}")
            return e
