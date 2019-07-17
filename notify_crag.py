import time
import sys
import yagmail
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
	yagmail.SMTP(myemail).send(sendemail, newtext)
	print('sent email')

time_to_sleep = 30 #sleep for 30 seconds before trying again
number_of_times_checked = 0
dates_of_interest = ['07/13/2019', '07/20/2019', '07/27/2019', '08/03/2019', '08/10/2019', '08/17/2019', '08/24/2019', '08/31/2019']

mailing_list = [line.rstrip('\n') for line in open('mailing_list.txt')]

inyo_wilderness_permit_code = "JM23"
driver = webdriver.Chrome()
driver.get("https://www.recreation.gov/permits/233262/registration/detailed-availability")


while(1):
	for date in dates_of_interest:
		# Choose date
		driver.find_element_by_xpath("//input[@aria-label='Date  - Enter a date or press the down arrow to interact with the calendar.']").send_keys(date)
		# Open filter selection
		driver.find_element_by_xpath("//button[@class='rec-button-tertiary rec-icon-left']").click()
		# Enter the trailhead of interest
		driver.find_element_by_id("division-search-input").send_keys(inyo_wilderness_permit_code)
		# Apply the filter
		driver.find_element_by_xpath("//button[@class='sarsa-button rec-button-primary sarsa-button-primary sarsa-button-md']").click()
		# Select number of people (1 minimum)
		driver.find_element_by_id('number-input').send_keys("1")
		# Select NO for this being a commercial trip
		driver.find_element_by_xpath("//div[@class='rec-form-inline-item-wrap']/div[2]/label[@class='rec-label-radio']/span[@class='rec-input-radio']").click()
		# Extract availability for date in question
		values = driver.find_element_by_xpath("//table[@class='rec-availability-table']/tbody/tr/td[4]")

		if "W" in values.text:
			print("Walk-up Only")
		else:
			#send email here
			print("Found " + values.text + "available spots")

		driver.refresh()
	time.sleep(time_to_sleep)