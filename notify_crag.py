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
    yagmail.SMTP(myemail).send(sendemail, newtext, "You only have a few minutes!\n\nLink: https://www.recreation.gov/permits/233262/registration/detailed-availability")
    print('sent email')

time_to_sleep = 30 #sleep for 30 seconds before trying again
number_of_times_checked = 0
dates_of_interest = ['07/27/2019', '08/03/2019', '08/10/2019', '08/17/2019', '08/24/2019', '08/31/2019']

mailing_list = [line.rstrip('\n') for line in open('mailing_list.txt')]

inyo_wilderness_permit_code = "JM23"
driver = webdriver.Chrome()
driver.get("https://www.recreation.gov/permits/233262/registration/detailed-availability")


while(1):
    for date in dates_of_interest:
        if(parse(str(dt.today())) <= parse(date)):
            # Choose date
            driver.find_element_by_xpath("//input[@aria-label='Date  - Enter a date or press the down arrow to interact with the calendar.']").send_keys(date)
            # Open filter selection
            driver.find_element_by_xpath("//button[@class='rec-button-tertiary rec-icon-left']").click()
            # Enter the trailhead of interest
            driver.find_element_by_id("division-search-input").send_keys(inyo_wilderness_permit_code)
            # Apply the filter
            driver.find_element_by_xpath("//button[@class='sarsa-button rec-button-primary sarsa-button-primary sarsa-button-md']").click()
            time.sleep(2) # Allow some time to fetch results
            # Select number of people (1 minimum)
            driver.find_element_by_id('number-input').send_keys("1")
            time.sleep(2) # Allow some time to fetch results
            # Select NO for this being a commercial trip
            driver.find_element_by_xpath("//*[@id='per-availability-main']/div/div[1]/div[2]/div/div/fieldset/div/div[2]").click()
            #driver.find_element_by_xpath("//div[@class='rec-form-inline-item-wrap']/div[2]/label[@class='rec-label-radio']/span[@class='rec-input-radio']").click()
            time.sleep(4) # Allow some time to fetch results
            # Extract availability for date in question
            values = driver.find_element_by_xpath("//table[@class='rec-availability-table']/tbody/tr/td[4]")

            if "W" in values.text:
                print("Walk-up Only")
            else:
                output_string = "Found " + values.text + " slots available for " + date
                for email in mailing_list:
                    Email(output_string, sendemail=email)

            driver.refresh()
    time.sleep(time_to_sleep)
