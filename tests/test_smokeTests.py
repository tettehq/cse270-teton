import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException


class TestSmokeTests():
    def setup_method(self, method):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 20)  # increased wait time
        self.driver.implicitly_wait(5)  # shorter implicit wait; explicit preferred

    def teardown_method(self, method):
        self.driver.quit()

    def wait_and_click(self, by, locator):
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()

    def wait_for_text(self, by, locator, text):
        self.wait.until(EC.text_to_be_present_in_element((by, locator), text))

    def test_directorypage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1936, 1096)

        self.wait_and_click(By.LINK_TEXT, "Directory")
        self.wait_and_click(By.ID, "directory-grid")

        text_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gold-member:nth-child(9) > p:nth-child(2)"))
        )
        assert text_element.text == "Teton Turf and Tree"

        self.wait_and_click(By.ID, "directory-list")

        text_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gold-member:nth-child(9) > p:nth-child(2)"))
        )
        assert text_element.text == "Teton Turf and Tree"

    def test_adminpage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1936, 1096)

        self.wait_and_click(By.LINK_TEXT, "Admin")

        label_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".myinput:nth-child(2)"))
        )
        assert label_element.text == "Username:"

        self.wait_and_click(By.ID, "username")
        self.driver.find_element(By.ID, "username").send_keys("aaa")
        self.driver.find_element(By.ID, "password").send_keys("1144")
        self.wait_and_click(By.CSS_SELECTOR, ".mysubmit:nth-child(4)")

        self.wait_for_text(By.CSS_SELECTOR, ".errorMessage", "Invalid username and password.")

    def test_homepagejoinuslinkspotlights(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1936, 1096)

        elements1 = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".spotlight1 > .centered-image"))
        )
        assert len(elements1) > 0

        elements2 = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".spotlight2 > .centered-image"))
        )
        assert len(elements2) > 0

        join_us_links = self.wait.until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, "Join Us!"))
        )
        assert len(join_us_links) > 0

        self.wait_and_click(By.LINK_TEXT, "Join Us!")

    def test_homepagesitelogotitleandheading(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1936, 1096)

        logo_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".header-logo img"))
        )
        assert len(logo_elements) > 0

        h1 = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".header-title > h1"))
        )
        assert h1.text == "Teton Idaho"

        h2 = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".header-title > h2"))
        )
        assert h2.text == "Chamber of Commerce"

        assert self.driver.title == "Teton Idaho CoC"

    def test_joinpage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1936, 1096)

        self.wait_and_click(By.LINK_TEXT, "Join")

        label = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".myinput:nth-child(2)"))
        )
        assert label.text == "First Name"

        self.wait_and_click(By.NAME, "fname")
        self.driver.find_element(By.NAME, "fname").send_keys("John")
        self.driver.find_element(By.NAME, "lname").send_keys("Doe")
        self.driver.find_element(By.NAME, "bizname").send_keys("Anonymous")
        self.driver.find_element(By.NAME, "biztitle").send_keys("Manager")
        self.driver.find_element(By.NAME, "submit").click()

        email_label = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".myinput:nth-child(2)"))
        )
        assert email_label.text == "Email"
