import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

DURATION_IN_MINS = 5
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://orteil.dashnet.org/experiments/cookie/")


class CookieClicker:
    def __init__(self, interval):
        self.check_int = interval
        self.duration = DURATION_IN_MINS
        self.cps = 0
        self.cookie = driver.find_element(by=By.ID, value="cookie")

    def click_cookie(self):
        """ "Clicke the cookie element on screen for the amount of time set by the chosen interval"""
        end = time.time() + self.check_int
        while True:
            self.cookie.click()
            if time.time() > end:
                break

    def quit(self):
        """Closes the Selenium browser"""
        driver.quit()

    def buy_power_up(self):
        """Searches for and buys the most expensive power up tat can be affored until fund are too low to continue"""
        while True:
            time.sleep(0.1)
            balance = int(
                driver.find_element(by=By.ID, value="money").text.replace(",", "")
            )
            power_ups = driver.find_elements(
                by=By.CSS_SELECTOR, value="div#store div b"
            )
            power_up_dict = {
                power_up.text.split("-")[0].strip(): int(
                    power_up.text.replace(",", "").split()[-1]
                )
                for power_up in power_ups
                if power_up.text != ""
            }
            costs = list(power_up_dict.values())
            names = list(power_up_dict.keys())
            buy = None
            for cost in costs:
                if balance >= cost:
                    buy = names[costs.index(cost)]
            if buy != None:
                driver.find_element(by=By.CSS_SELECTOR, value=f"div#buy{buy}").click()
            balance = int(
                driver.find_element(by=By.ID, value="money").text.replace(",", "")
            )
            min_power_up_cost = min(list(power_up_dict.values()))
            if balance < min_power_up_cost:
                break

    def cookies_per_sec(self):
        """Returns a string that contains the cookies per second"""
        self.cps = driver.find_element(
            by=By.CSS_SELECTOR, value="div#cps"
        ).text.split()[-1]
        return f"Cookies Per Second {self.cps}"

    def start(self):
        """Loops through clicking and buying power up for the set duration"""
        end = time.time() + (60 * self.duration)
        while True:
            self.click_cookie()
            self.buy_power_up()
            if time.time() >= end:
                break
