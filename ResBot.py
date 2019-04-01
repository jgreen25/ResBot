from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

class ResBot():
	def __init__(self, url, acnt_status, date_time, day_limit, seats, \
            email = None, password = None, number = None):
	    self.url = url
	    self.acnt_status = acnt_status
	    self.date_time = date_time
        self.day_limit = day_limit
        self.seats = seats
	    self.email = email
	    self.password = password
        self.number = number
	    options = webdriver.ChromeOptions()
	    options.add_argument('headless')
	    self.driver = webdriver.Chrome(chrome_options = options)

    def resy_login(self, email, password):
        try:
            current_time = datetime.datetime.now()
            self.driver.get(self.url + 'date=' + current_time[:10] \
                + '&seats=' + self.seats)
        except:
            time = datetime.datetime.now() + datetime.timedelta(3)
            self.driver.get(self.url + 'date=' + time[:10] \
                + '&seats=' + self.seats)
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
            if current_time + datetime.timedelta(self.day_limit) \
                    > self.date_time:
                break
        self.driver.get(self.url + 'date=' + self.date_time[:10] \
            + '&seats=' + self.seats)
        times = self.driver.find_elements_by_class_name('time')
        for i in range(len(times)):
            if times[i].getText() == self.make_time(self.date_time):
                time = times[i]
                time.find_element_by_xpath('./../..').click()
                ########### start here #############

    def make_time(self, date_time):
        time = date_time[11:16]
        if int(time[:2]) > 12:
            time = str(int(time[:2]) - 12) + time[2:] + 'PM'
        else:
            time += 'AM'
        return time