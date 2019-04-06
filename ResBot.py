from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


class ResBot():
    def __init__(self, url, acnt_status, date_time, day_limit, seats, \
            card_number, card_exp, card_cvv, email = None, \
            password = None, number = None):
        self.url = url
        self.acnt_status = acnt_status
        self.date_time = date_time
        self.day_limit = day_limit
        self.seats = seats
        self.card_number = card_number
        self.card_exp = card_exp
        self.card_cvv = card_cvv
        self.email = email
        self.password = password
        self.number = number
        #options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        #self.driver = webdriver.Chrome(chrome_options = options)
        self.driver = webdriver.Chrome() ####

    def resy_login(self, email, password):
        try:
            current_time = str(datetime.datetime.now())
            self.driver.get(self.url + 'date=' + current_time[:10] \
                + '&seats=' + self.seats)
        except:
            time = str(datetime.datetime.now() + datetime.timedelta(3))
            self.driver.get(self.url + 'date=' + time[:10] \
                + '&seats=' + self.seats)
        log_in  = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.ResyProfileMenu__log-in.no-animate')))
        log_in.click()
        by_email_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, \
            "//button[contains(text(), 'Use Email and Password instead')]")))
        by_email_btn.send_keys(Keys.ENTER)
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, \
            "//input[@name='email']")))
        email_input.send_keys(email)
        self.driver.find_element_by_name('password').send_keys(
            password)
        self.driver.find_element_by_class_name('Button').click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, \
            'profileMenu')))
        return
    
    def resy_make_res(
            self, date_time, day_limit, seats, card_number, card_exp, card_cvv):
        while True:
            current_time = datetime.datetime.now()
            if current_time + datetime.timedelta(day_limit) \
                    > date_time:
                break
        self.driver.get(self.url + 'date=' + str(date_time)[:10] \
            + '&seats=' + seats)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.time')))
        times = self.driver.find_elements_by_css_selector('.time')
        for i in range(len(times)):
            if times[i].text == self.make_time(date_time):
                time = times[i]
                break
        time.find_element_by_xpath('../..').click()
        iframe = self.driver.find_elements_by_tag_name('iframe')[1]
        self.driver.switch_to_frame(iframe)
        reserve_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.legal')))
        try:
            cards = self.driver.find_elements_by_tag_name('option')
        except:
            cards = []
        button = self.driver.find_element_by_css_selector('.book-reservation')
        button.find_elements_by_xpath('.//*')[5].click()
        if len(cards) == 1:
            self.driver.find_element_by_id('credit-card-number').send_keys(
                card_number)
            self.driver.find_element_by_id('expiration').send_keys(
                card_exp)
            self.driver.find_element_by_id('cvv').send_keys(card_cvv)
            self.driver.find_element_by_class_name('primary').click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, \
            '.special-request')))
        return
            
    def make_time(self, date_time):
        time = str(date_time)[11:16]
        if int(time[:2]) > 12:
            time = str(int(time[:2]) - 12) + time[2:] + 'PM'
        elif int(time[:2]) == 12:
            time += 'PM'
        else:
            time += 'AM'
        return time


def main():
    date_time = datetime.datetime(2019, 4, 8, 12)
    bot = ResBot(
        'https://resy.com/cities/atx/odd-duck?', \
        True, date_time, 4, '2', '4900710010458914', '1120', '602', \
        'jgreen25tu@gmail.com', 'hawkeny0GHM', '6785758996')
    print("Bot created.")
    bot.resy_login(bot.email, bot.password)
    print("Logged in.")
    bot.resy_make_res(bot.date_time, bot.day_limit, bot.seats, bot.card_number, \
        bot.card_exp, bot.card_cvv)
    print("Reservation made.")
    return

if __name__ == '__main__':
    main()