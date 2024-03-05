import os
import time

import undetected_chromedriver as uc
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SetupDriver:
    def __init__(self, url: str, selenoid: bool = False, headless: bool = False):
        self.driver = None
        self._url = url
        self.headless = headless
        self.selenoid = selenoid

    def __enter__(self):
        return self.driver

    def __exit__(self):
        self.driver.quit()

    def wait_loads(self, tm=3) -> None:
        try:
            self.wait_web_driver(60).until(
                lambda a: self.driver.execute_script("return document.readyState==\"complete\";"))
        except Exception as e:
            logger.error(f"Error waiting for page to load: {e}")
        time.sleep(tm)

    def wait_web_driver(self, tm: int = 5) -> WebDriverWait:
        try:
            return WebDriverWait(self.driver, tm, poll_frequency=1)
        except Exception as e:
            logger.error(f"Error waiting for WebDriver: {e}")

    def wait_xpath(self, path: str, tm=20) -> webdriver:
        element = self.wait_web_driver(tm).until(EC.visibility_of_element_located((By.XPATH, path)))
        return element

    def start_driver(self) -> webdriver:
        logger.info(f"Starting driver for {self._url}")
        return self.driver.get(self._url)

    def open_page(self, page: str) -> webdriver:
        self.driver.get(page)
        self.driver.implicitly_wait(2)
        self.wait_loads()
        return self.driver

    def setup(self, host: str, name: str = "default") -> webdriver:
        """Setup selenium driver"""

        if self.selenoid:
            web_options = webdriver.ChromeOptions()
            web_options.add_argument("--verbose")
            web_options.add_argument("--no-sandbox")
            web_options.add_argument("disable-infobars")
            web_options.add_argument("--disable-extensions")
            web_options.add_argument("--disable-notifications")
            web_options.add_argument("--disable-gpu")
            web_options.add_experimental_option("useAutomationExtension", False)
            web_options.set_capability(
                name="selenoid:options",
                value={
                    "browserName": "chrome",
                    "version": "110.0",
                    "enableVNC": True,
                    "enableVideo": False,
                    "screenResolution": "1920x1080x24",
                    "sessionTimeout": "2m",
                    "name": name,
                    "timeZone": "São Paulo/Brazil"
                }
            )
            self.driver = webdriver.Remote(command_executor=f'http://{host}:4444/wd/hub', options=web_options)
            self.driver.maximize_window()
        else:
            uc_options = uc.ChromeOptions()
            uc_options.add_argument("--no-sandbox")
            uc_options.add_argument("disable-infobars")
            uc_options.add_argument("--disable-extensions")
            uc_options.add_argument("--disable-gpu")
            uc_options.headless = self.headless

            path = os.path.join(os.getcwd(), "output")
            prefs = {
                "download.default_directory": path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
            }
            uc_options.add_experimental_option("prefs", prefs)
            self.driver = uc.Chrome(options=uc_options)
            self.driver.maximize_window()

        self.driver.implicitly_wait(10)
        return self.driver
