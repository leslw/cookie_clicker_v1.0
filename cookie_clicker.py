import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

DURATION_IN_MINS = 5
POWER_UP_CHECK_INTERVAL_IN_SECS = 30

class CookieClicker:
    def __init__(self, interval):
        self.check_interval = interval
        self.duration = DURATION_IN_MINS
        self.cps = 0
        self.cookie = None

    def initialize_driver(self):
        # Set up the Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://orteil.dashnet.org/experiments/cookie/")
        self.cookie = self.driver.find_element(by=By.ID, value="cookie")

    def click_cookie(self):
        # Click the cookie element repeatedly for the specified interval
        end_time = time.time() + self.check_interval
        while time.time() < end_time:
            self.cookie.click()

    def buy_power_up(self):
        # Search for and purchase the most expensive affordable power-up
        while True:
            time.sleep(0.1)
            balance = int(self.driver.find_element(by=By.ID, value="money").text.replace(",", ""))
            power_up_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value="div#store div b")
            power_up_dict = {}
            for power_up in power_up_elements:
                text = power_up.text
                if text != "":
                    name, cost = text.split("-")[0].strip(), int(text.replace(",", "").split()[-1])
                    power_up_dict[name] = cost
            affordable_power_ups = [name for name, cost in power_up_dict.items() if balance >= cost]
            if affordable_power_ups:
                self.driver.find_element(by=By.CSS_SELECTOR, value=f"div#buy{affordable_power_ups[-1]}").click()
            balance = int(self.driver.find_element(by=By.ID, value="money").text.replace(",", ""))
            min_power_up_cost = min(power_up_dict.values())
            if balance < min_power_up_cost:
                break

    def get_cookies_per_sec(self):
        # Retrieve and return the current cookies per second value
        cps_element = self.driver.find_element(by=By.CSS_SELECTOR, value="div#cps")
        self.cps = float(cps_element.text.split()[-1])
        return self.cps

    def start(self):
        # Start the game by clicking the cookie and buying power-ups for the specified duration
        self.initialize_driver()
        end_time = time.time() + (60 * self.duration)
        while time.time() < end_time:
            self.click_cookie()
            self.buy_power_up()

    def quit(self):
        # Close the Selenium browser
        self.driver.quit()
