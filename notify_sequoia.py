import time
from dateutil.parser import parse
from datetime import date as dt
import sys
import yagmail
import getpass
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

def Email(newtext, myemail=None, password=None, sendemail=None):
    if myemail == None:
        myemail = str(open("email.txt", 'r').read()).partition(':')[0]
    if password == None:
        password = str(open("email.txt", 'r').read()).partition(':')[2]
    if sendemail == None:
        print("error")
    yagmail.register(myemail, password)
    yag = yagmail.SMTP(myemail)
    yagmail.SMTP(myemail).send(sendemail, newtext, "You only have a few minutes!\n\nLink: https://www.recreation.gov/permits/233260")
    print('sent email')

time_to_sleep = 60 #sleep for 60 seconds before trying again
number_of_times_checked = 0
dates_of_interest = ['07/31/2020', '08/01/2020']

mailing_list = [line.rstrip('\n') for line in open('mailing_list.txt')]

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('log-level=3')
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.recreation.gov/camping/campgrounds/232461/availability")
#driver = webdriver.Chrome(chrome_options=options)
#driver.get("https://www.recreation.gov/camping/campgrounds/232461/availability")
#driver = webdriver.Chrome(chrome_options=options)
#driver.get("https://www.recreation.gov/camping/campgrounds/232461/availability")

while(1):
    for date in dates_of_interest:
        if(parse(str(dt.today())) <= parse(date)):
            time.sleep(4) # Allow some time to fetch results
            
            #First set the date to the desired date
            driver.find_element_by_xpath("//*[@id='single-date-picker-1']").send_keys(date)
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='single-date-picker-1']").send_keys(Keys.CONTROL,"a")
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='single-date-picker-1']").send_keys(date)
            time.sleep(4)
            
            for row in range(2408,2508):
                result = driver.find_element_by_xpath("//*[@id='" + str(row) + "']/td[2]/div/button").get_attribute('aria-label')
                if("is available" in result):
                    output_string = "Lodgepole Campground: " + result
                    for email in mailing_list:
                        Email(output_string, sendemail=email)
                else:
                    print(result)

            driver.refresh()
    time.sleep(time_to_sleep)