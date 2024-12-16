import time 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd 

driver = webdriver.Chrome()
wait = WebDriverWait(driver,20)

driver.get('https://www.linkedin.com/')
time.sleep(2)

sign_in_with_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
sign_in_with_email_button.click()
print("Button clicked successfully!")
time.sleep(2)

email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
email_input.send_keys('prasanth33460@gmail.com')
print("Email entered Successfully!")
time.sleep(2)

password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
password_input.send_keys('prasanthXbezos@1234509876')
print("Password entered Successfully!")
time.sleep(2)

sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
sign_in_button.click()
print("Sign in Button clicked!")
time.sleep(2)

try:
    otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
    print("Please enter the OTP in the browser...")
    wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
    print(f"OTP detected: {otp_input.get_attribute('value')}")
    time.sleep(2)

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
    submit_button.click()
    print("Submit button clicked successfully!")
    time.sleep(2)

except Exception as otp_exception:
    print("OTP step skipped or not required.")
    
driver.maximize_window()

job_url = 'https://www.linkedin.com/my-items/posted-jobs/?jobState=CLOSED'
driver.get(job_url)

while True:
    try:
        job_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'BtboaOZvCbDyiBLJYsPvSBkZqJdTJHqbmLY')]//a[contains(@class, 'afaFOTlZPsCzjvRLucMiKLrwEMAMHRDLkDjhg')]")))

        if job_links:
            first_job_link = job_links[0]
            first_job_url = first_job_link.get_attribute("href")
            print(f"Clicking on Job URL: {first_job_url}")
            first_job_link.click()

            time.sleep(3)  
            print("Job page opened successfully.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        break

view_applicants_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'mr2') and .//span[text()='View applicants']]")))
view_applicants_button.click()

soup = BeautifulSoup(driver.page_source, 'lxml')
