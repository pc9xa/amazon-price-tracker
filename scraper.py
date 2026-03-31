import arrow
import database as db
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless=new")  # The magic line to hide the window
        self.chrome_options.add_argument("--disable-gpu")  # Recommended for headless performance
        self.chrome_options.add_argument("--window-size=1920,1080")  # Set a size so the layout stays consistent
        self.chrome_options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36")
        self.chrome_options.add_argument("--profile-directory=Default")
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 2)

    def open_product_link(self, product_url):
        self.start_driver()
        self.driver.get(product_url)

        try:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.a-button-text')))
        except TimeoutException:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span#productTitle')))
        else:
            continue_button = self.driver.find_element(By.CSS_SELECTOR, 'button.a-button-text')
            continue_button.click()
        finally:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span#productTitle')))

    def get_product_screenshot(self, product_url):
        self.open_product_link(product_url)
        screenshot = self.driver.get_screenshot_as_png()
        self.driver.close()
        return screenshot

    def save_product(self, product_url):
        # Scrape product info
        self.open_product_link(product_url)
        product_name = self.driver.find_element(By.CSS_SELECTOR, 'span#productTitle').text
        product_price_whole = self.driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
        product_price_fraction = self.driver.find_element(By.CSS_SELECTOR, 'span.a-price-fraction').text
        product_price = product_price_whole.replace(',', '') + '.' + product_price_fraction

        # Get time now
        local = arrow.utcnow().to('Asia/Manila')
        timestamp = local.format()

        # Save product info to DB
        db.save_price(product_name, product_price, timestamp)

        self.driver.quit()

    @staticmethod
    def load_all_tracked_products():
        return db.load_tracked_products()

    @staticmethod
    def get_product_list_size():
        return len(db.load_tracked_products())

    @staticmethod
    def load_product_info(product):
        return db.load_product_prices(product)

    @staticmethod
    def del_one_product(product):
        db.del_product(product)

    @staticmethod
    def init_db():
        db.init_db()