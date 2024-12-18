import random 
import time 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd 

random_sleep_time = random.uniform(1, 5)

driver = webdriver.Chrome()
wait = WebDriverWait(driver,20)

driver.get('https://www.linkedin.com/')
time.sleep(random_sleep_time)

sign_in_with_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
sign_in_with_email_button.click()
print("Button clicked successfully!")
time.sleep(random_sleep_time)

email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
email_input.send_keys('prasanth33460@gmail.com')
print("Email entered Successfully!")
time.sleep(random_sleep_time)

password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
password_input.send_keys('prasanthXbezos@1234509876')
print("Password entered Successfully!")
time.sleep(random_sleep_time)

sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
sign_in_button.click()
print("Sign in Button clicked!")
time.sleep(random_sleep_time)

try:
    otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
    print("Please enter the OTP in the browser...")
    wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
    print(f"OTP detected: {otp_input.get_attribute('value')}")
    time.sleep(random_sleep_time)

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
    submit_button.click()
    print("Submit button clicked successfully!")
    time.sleep(random_sleep_time)

except Exception as otp_exception:
    print("OTP step skipped or not required.")
    
driver.maximize_window()

job_url = 'https://www.linkedin.com/my-items/posted-jobs/'
driver.get(job_url)

while True:
    try:
        link_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'DJwghvRgvkwPahDncmLgkUmsEvYQAKeTec')]//a")))

        for link in link_elements:
            link_text = link.text.strip()
            link_href = link.get_attribute("href")
            print(f"Clicking on link: {link_text} ({link_href})")
            ActionChains(driver).move_to_element(link).perform()
            link.click()
            time.sleep(random_sleep_time)
            break
        print("Link clicked successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        break

view_applicants_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'mr2') and .//span[text()='View applicants']]")))
view_applicants_button.click()
time.sleep(random_sleep_time)

def parse_applicants():
    try:
        applicants = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'hiring-applicants__list-item')]//a")))
        
        for index, applicant in enumerate(applicants, start=1):
            time.sleep(random_sleep_time)
            applicant.click()
            
            name = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'hiring-applicant-header')]//h1"))).text
            applicant_name = name.split("’s application")[0] 
            location = driver.find_element(By.XPATH, "//*[contains(@class, 'hiring-applicant-header')]//div[contains(@class, 't-16')][2]").text
            
            more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'hiring-applicant-header-actions')]//button[contains(@class, 'artdeco-dropdown__trigger')]//span[text()='More…']")))
            more_button.click()
            
            email = None
            try:
                email_element = wait.until(EC.presence_of_element_located((By.XPATH, "//li[a[contains(@href, 'mailto:')]]//span[@class='hiring-applicant-header-actions__more-content-dropdown-item-text' and @aria-hidden='true']")))
                email = email_element.text.strip()
            except:
                email = "Not Available"
            
            phone_number = None
            try:
                phone_element = wait.until(EC.presence_of_element_located((By.XPATH, "//li[div[contains(@class, 'artdeco-dropdown__item')]]//span[contains(@class, 'hiring-applicant-header-actions__more-content-dropdown-item-text')]")))
                phone_number = phone_element.text.strip()
            except:
                phone_number = "Not Available"

            print(f"Applicant Number {index}:")
            print(f"Name: {applicant_name}")
            print(f"Location: {location}")
            print(f"Email: {email}")
            print(f"Phone Number: {phone_number}")
            print("-" * 40)
        
        time.sleep(random_sleep_time)
            
    except Exception as e:
        print(f"An error occurred: {e}")

