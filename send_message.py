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


HEADLESS = True
CONTACTS_URL = "https://sheetdb.io/api/v1/hws5wv565i8fz"
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
	webdriver.Firefox(executable_path='/home/saquib/Downloads/whatsapp-ng-automation/geckodriver')
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
	try:
		messageBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, MESSAGE_BOX_SELECTOR)))
		messageBox.click()
		messageBox.send_keys("Hello!")
		line_break(driver)
		messageBox.send_keys("आशा है कि आप हमारे ऑनलाइन कार्यक्रम में कोडिंग सीख रहे हैं।")
		line_break(driver)
		messageBox.send_keys("यदि आप हमारे 1 साल के आवासीय कार्यक्रम में शामिल होना चाहते हैं, सॉफ्टवेयर इंजीनियरिंग में  गारंटीकृत नौकरियां प्राप्त करना चाहते हैं और प्रति माह  Rs 20000-40000 के बीच  कमाना चाहते हैं, कृपया इस लिंक पर क्लिक करें रजिस्टर करने के लिए:")
		line_break(driver)
		messageBox.send_keys("http://admissions.navgurukul.org/partnerLanding/chirag")
		line_break(driver)
		messageBox.send_keys("हमारे 1 वर्ष के आवासीय कार्यक्रम के बारे में जानने के लिए, नीचे दिए गए वीडियो देखें")
		line_break(driver)
		messageBox.send_keys("https://youtu.be/HjqfZ-Matyk")
		send_message(driver)
	except:
		print("Number is invalid, skipping")


def send_message(driver):
	wait = WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)
	sendBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SEND_BUTTON_SELECTOR)))
	sendBox.click()

def get_next_number():
	response = requests.get(CONTACTS_URL)
	if response.status_code != 200:
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
		logging.info("Sent!")

	driver.close()





