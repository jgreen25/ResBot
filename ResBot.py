from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


class ResBot():
    def __init__(self, url, date_time, day_limit, seats, \
            card_number, card_exp, card_cvv, cancel_fee, \
            email = None, password = None):
        self.url = url
        self.date_time = date_time
        self.day_limit = day_limit
        self.seats = seats
        self.__card_number = card_number
        self.__card_exp = card_exp
        self.__card_cvv = card_cvv
        self.cancel_fee = cancel_fee
        self.__email = email
        self.__password = password
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.__driver = webdriver.Chrome(chrome_options = options)

    def resy_login(self, url, seats):
        current_time = str(datetime.datetime.now())
        self.__driver.get(url + 'date=' + current_time[:10] \
            + '&seats=' + seats)
        log_in  = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.ResyProfileMenu__log-in.no-animate')))
        log_in.click()
        by_email_btn = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.XPATH, \
            "//button[contains(text(), 'Use Email and Password instead')]")))
        by_email_btn.send_keys(Keys.ENTER)
        email_input = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.XPATH, \
            "//input[@name='email']")))
        email_input.send_keys(self.__email)
        self.__driver.find_element_by_name('password').send_keys(
            self.__password)
        self.__driver.find_element_by_class_name('Button').click()
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, \
            'profileMenu')))
        return
    
    def resy_make_res(self, date_time, day_limit, seats, cancel_fee):
        while True:
            current_time = datetime.datetime.now()
            if current_time + datetime.timedelta(day_limit) \
                    > date_time:
                break
        self.__driver.get(self.url + 'date=' + str(date_time)[:10] \
            + '&seats=' + seats)
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.time')))
        times = self.__driver.find_elements_by_css_selector('.time')
        for i in range(len(times)):
            if times[i].text == self._make_time(date_time):
                time = times[i]
                break
        time.find_element_by_xpath('../..').click()
        iframe = self.__driver.find_elements_by_tag_name('iframe')[1]
        self.__driver.switch_to_frame(iframe)
        reserve_btn = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.legal')))
        if cancel_fee == True:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, \
                '//option')))
            cards = self.__driver.find_elements_by_xpath('//option')
        else:
            cards = []
        button = self.__driver.find_element_by_css_selector('.book-reservation')
        children = button.find_elements_by_xpath('.//*')
        for child in children:
            try:
                child.click()
            except:
                continue
        if len(cards) == 1:
            card_num = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, \
                'credit-card-number')))
            card_num.send_keys(self.__card_number)
            self.__driver.find_element_by_id('expiration').send_keys(
                self.__card_exp)
            self.__driver.find_element_by_id('cvv').send_keys(self.__card_cvv)
            self.__driver.find_element_by_class_name('primary').click()
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.special-request')))
        self.__driver.quit()
        return

    def open_table_login(self, url):
        self.__driver.get(url)
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, \
            'glocal_nav_sign_in')))
        ################ continue here ##################
        return

    def open_table_make_res(self):
        pass
            
    def _make_time(self, date_time):
        time = str(date_time)[11:16]
        if int(time[:2]) > 12:
            time = str(int(time[:2]) - 12) + time[2:] + 'PM'
        elif int(time[:2]) == 12:
            time += 'PM'
        else:
            time += 'AM'
        return time


def main():
    pass

if __name__ == '__main__':
    main()