import time
from dateutil.parser import parse
from datetime import date as dt
import sys
import yagmail
import getpass
from selenium import webdriver
from selenium.webdriver.support.select import Select

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

time_to_sleep = 30 #sleep for 30 seconds before trying again
number_of_times_checked = 0
dates_of_interest = ['Saturday, July 27, 2019', 'Saturday, August 3, 2019', 'Saturday, August 10, 2019', 'Saturday, August 17, 2019', 'Saturday, August 24, 2019', 'Saturday, August 31, 2019']

mailing_list = [line.rstrip('\n') for line in open('mailing_list.txt')]

driver = webdriver.Chrome()
driver.get("https://www.recreation.gov/permits/233260")

while(1):
    for type in '12':
        for date in dates_of_interest:
            if(parse(str(dt.today())) <= parse(date)):
                time.sleep(4) # Allow some time to fetch results
                driver.find_element_by_id('division-selection-select').click()
                #select the item in drop-down for type of permit (day vs overnight)
                driver.find_element_by_xpath("//div[@id='division-selection']/div/div/ul/li[" + type + "]").click()
                time.sleep(4) # Allow some time to fetch results
                driver.find_element_by_id('number-input').send_keys("1") #select number of people, 1 is minimum
                #fetch the availability for the specified date
                availability = driver.find_element_by_xpath("//button[@aria-label='" + date + "']/div[1]/div[1]").get_attribute('aria-label')

                if("Available" in availability):
                    output_string = "Found " + availability.split()[2] + " slots available for " + date
                    for email in mailing_list:
                        Email(output_string, sendemail=email)
                else:
                    print("Sorry, nothing available")

                driver.refresh()
    time.sleep(time_to_sleep)