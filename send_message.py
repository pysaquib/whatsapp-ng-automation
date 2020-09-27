import logging
import json
import time
import requests
from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common import keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO)


HEADLESS = TRUE
CONTACTS_URL = "https://sheetdb.io/api/v1/l2wmtxqv959h7"
DEFAULT_WAIT_TIMEOUT = 30

MESSAGE_BOX_SELECTOR = "#main > footer > div._3ee1T._1LkpH.copyable-area > div._3uMse > div > div._3FRCZ.copyable-text.selectable-text"
SEND_BUTTON_SELECTOR = "#main > footer > div._3ee1T._1LkpH.copyable-area > div:nth-child(3) > button"
SIDE_PANE_SELECTOR = "#pane-side"
QR_CODE_SELECTOR = "._1QMFu > canvas:nth-child(3)"



def whatsapp_login_required(driver, number, timeout=DEFAULT_WAIT_TIMEOUT):
	driver.get("https://web.whatsapp.com/send?phone=+91{number}".format(number=number))
	started_at = time.time()
	while True:
		if driver.find_elements_by_css_selector(SIDE_PANE_SELECTOR):
			return False
		elif driver.find_elements_by_css_selector(QR_CODE_SELECTOR):
			driver.get_screenshot_as_file("login_%s.png"%int(started_at))
			return True	
		elapsed = time.time() - started_at 
		if elapsed > timeout:
			raise Exception("Timed out. Could not open page within %s seconds"%timeout)


def build_driver(headless):
	options = webdriver.FirefoxOptions() 
	if headless:
		options.add_argument("--headless")  
	return webdriver.Firefox(options=options)


def line_break(driver):
	actions = ActionChains(driver)
	actions.key_down(keys.Keys.SHIFT)
	actions.send_keys(keys.Keys.ENTER)
	actions.send_keys(keys.Keys.ENTER)
	actions.key_up(keys.Keys.SHIFT)
	actions.perform()


def type_message(driver):
	wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)
	messageBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, MESSAGE_BOX_SELECTOR)))
	messageBox.click()
	messageBox.send_keys("Hello!")
	line_break(driver)
	messageBox.send_keys("Testing.")

def send_message(driver):
	wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)

	sendBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SEND_BUTTON_SELECTOR)))
	sendBox.click()

def get_next_number():
	response = requests.get(CONTACTS_URL)
	if response.status_code is not 200:
		raise Exception("Could not fetch contacts. Got %s response"%response.status_code)
	contacts = json.loads(response.content)
	for contact in contacts:
		yield contact


if __name__ == '__main__':
	driver = build_driver(headless=True)
	
	for contact in get_next_number():
		logging.info("Sending to %s %s... "%(contact["Number"], contact["Name"]))
		if whatsapp_login_required(driver, contact["Number"]):
			logging.warning("Login Required. Press enter after Login...")
			input()

		type_message(driver)
		send_message(driver)
		logging.info("Sent!")

	driver.close()





