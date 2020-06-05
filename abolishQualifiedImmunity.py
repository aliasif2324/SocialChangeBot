from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import os, sys
import time,requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

class ReCaptcha:
	url_request = "http://2captcha.com/in.php"
	url_response = "http://2captcha.com/res.php"
	api_key = "80d2e64a3919bdfef42a4a072ef1c887"

	def __init__(self, method, google_key, page_url, tag):
		self.method = method
		self.google_key = google_key
		self.page_url = page_url
		self.tag = tag

	def request(self):
		task_id = 0
		payload = {
			'key': self.api_key,
			'invisible': 1,
			'method': self.method,
			'googlekey': self.google_key,
			'pageurl': self.page_url,
		}
		r = requests.get(self.url_request, params=payload)
		if r.status_code != 200:
			print(self.tag + 'Error to connect to server Captcha')
		else:
			if r.text == 'ERROR_ZERO_BALANCE':
				print(self.tag + "your balance isn\'t engough")
				return task_id
			data = r.text.split('|')
			if len(data) == 0:
				print(self.tag + 'Error get task id from server captcha')
				return task_id
			if data[0] == 'OK':
				task_id = data[1]
			else:
				print(self.tag + 'Error server Captcha, error get task id')
		return task_id

	def get_response(self, task_id):
		token = ''
		if task_id == 0:
			print(self.tag + 'Error server Captcha')
		else:
			payload = {'key': self.api_key,
					   'action': 'get',
					   'id': task_id}
			r = requests.get(self.url_response, params=payload)
			if r.text == 'CAPCHA_NOT_READY':
				pass
			else:
				data = r.text.split('|')
				if data[0] == 'OK':
					token = data[1]
				else:
					print(self.tag + 'Cannot resolve captcha on server')
		return token

delayTime = 2
audioToTextDelay = 200
filename = 'test.mp3'
byPassUrl = 'https://www.google.com/recaptcha/api2/demo'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

option = webdriver.ChromeOptions()
#option.add_argument('--disable-notifications')
#option.add_argument("--mute-audio")
# # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")

def solver_captcha():
    re_captcha = ReCaptcha('userrecaptcha', '6LdNvSkTAAAAAOyI81TRnGAYYz58AKpPUbWqUSbd', 'https://lofgren.house.gov/', '')
    task_id = re_captcha.request()
    captcha_token = re_captcha.get_response(task_id)
    i = 0
    print('Passing the captcha...')
    while captcha_token == '': 
        i += 1
        time.sleep(5)
        captcha_token = re_captcha.get_response(task_id)
    print('Passed captcha')
    driver.execute_script("arguments[0].value = arguments[1];", driver.find_element_by_id('g-recaptcha-response'), captcha_token)

def audioToText(mp3Path):

    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])

    driver.get(googleIBMLink)

    # Upload file 
    time.sleep(1)
    root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(mp3Path)

    # Audio to text is processing
    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[6]/div/div/dialog').find_elements_by_tag_name('dd')
    result = " ".join( [ each.text for each in text ] )

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
driver.get('https://lofgren.house.gov/contact')

zipCode = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "required-zip5")))
zipCode.send_keys('95135')
zipCode.send_keys(Keys.ENTER)

prefix = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-honorific-prefix")))
prefix.send_keys('M')

first = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-first")))
first.send_keys('First')

last = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-last")))
last.send_keys('Last')

street = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-address")))
street.send_keys('3248 Altia Street')

city = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-city")))
city.send_keys('San Jose')

email = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-valid-email")))
email.send_keys('test123@gmail.com')

phone = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-phone")))
phone.send_keys('4057324521')

concern = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-issue")))
concern.send_keys('O')

msg = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "required-message")))
msg.send_keys('test')

solver_captcha()

driver.find_element_by_id('submit').click()