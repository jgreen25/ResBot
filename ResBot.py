from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

class ResBot():
	def __init__(self, url, acnt_status, date_time, day_limit, email = None, \
		    password = None, number = None):
	    self.url = url
	    self.acnt_status = acnt_status
	    self.date_time = date_time
        self.day_limit = day_limit
	    self.email = email
	    self.password = password
        self.number = number
	    options = webdriver.ChromeOptions()
	    options.add_argument('headless')
	    self.driver = webdriver.Chrome(chrome_options = options)

    def resy_login(self, email, password):
        self.driver.get(self.url)
        self.driver.find_element_by_class_name(
        	'ResyProfileMenu__log-in no-animate').click()
        self.driver.find_elements_by_tag_name('button')[1].click()
        self.driver.find_element_by_name('email').send_keys(
            email)
        self.driver.find_element_by_name('password').send_keys(
            password)
        self.driver.find_element_by_class_name('Button').click()
        return
    
    def resy_make_res(self, datetime):
        self.driver.find_element_by_class_name('ResyButton').click()
        while True:
            current_time = datetime.datetime.now()
            if current_time + datetime.timedelta(self.day_limit) > self.date_time:
                break
        
