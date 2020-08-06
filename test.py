from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, random, sys


# test.py 5555555555 'Your message to send out'
the_number = sys.argv[1]    # phone number to send a Text to
the_message = sys.argv[2]   # message to send to the phone number

driver = webdriver.Firefox(executable_path='geckodriver.exe')   # make sure the geckodriver is in the same folder
driver.get('https://www.textnow.com/login')                     # login page for TextNow

timeout = 30        # 30 sec timeout -- in case their browser is laggy
try:
    # waiting until the TEXTBOX with the ID 'txt-username' has loaded on the page..
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "txt-username")))
except TimeoutException:
    driver.quit()       # if it wasn't found.. quit.

with open('login.txt') as f:        # login information stored here as   email:password
    login = f.read().split(':')     # split the login data into 2 items
email = login[0]                    # grab the email (aka before the :  )
password = login[1]                 # grab the password  (aka after the :  )

# find the username/email field to login with
user = driver.find_element_by_id('txt-username')
user.clear()
user.send_keys(email)
# find the password field for logging in
passw = driver.find_element_by_id('txt-password')
passw.clear()
passw.send_keys(password)
# find the LOGIN button and click it.
login = driver.find_element_by_id('btn-login')
login.click()

time.sleep(1)

print("Looking for the NEW TEXT button...")

# let's send a new text...

timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "newText")))
except TimeoutException:
    driver.quit()

user = driver.find_element_by_id('newText')
user.click()

time.sleep(1)

print("Looking for SEND TO input...")
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "newConversationTextField")))
    sendTo = driver.find_element_by_class_name('newConversationTextField')
    sendTo.send_keys(the_number)
    time.sleep(1)
except TimeoutException:
    driver.quit()

print("trying to find the message input area...")
time.sleep(2)

try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "text-input")))
    text_inner = driver.find_element_by_id('text-inner')
    text_inner.click()
    textInput = driver.find_element_by_id('text-input')
    textInput.click()
    time.sleep(1)
    print("---------")
    print("FOUND INPUT AREA !!!")
    print("")
    #textInput.send_keys("let's try and test this thing out... ")
    textInput.clear()
    textInput.click()
    textInput.send_keys(the_message)

    time.sleep(1)
    textInput.send_keys(Keys.ENTER)

except TimeoutException:
    driver.quit()


print("all done... did it work?!?!?!?!")
