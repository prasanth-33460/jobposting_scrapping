import random 
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import WebDriverException

class LoginModule:
    def __init__(self,base_url,email,password):
        self.base_url = base_url
        self.email = email
        self.password = password
        
        try:
            self.driver = webdriver.Chrome() 
            self.wait = WebDriverWait(self.driver, 20)
        except WebDriverException as e:
            print("Failed to initialise webdriver")
        
    def random_sleep(self):
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)
        
    def open_page(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.base_url)
        except Exception as e:
            print("Failed to open")
            
    def sign_in_with_email_btn(self):
        try:
            sign_in_with_email_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
            sign_in_with_email_button.click()
            print("Button clicked successfully!")
            self.random_sleep()
        except Exception as e:
            print("Failed to click on sign in")
            
    def enter_email(self):
        try:
            email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
            email_input.send_keys(self.email)
            print("Email entered Successfully!")
            self.random_sleep()
        except Exception as e:
            print("failed to enter email")
            
    def enter_password(self):
        try:
            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
            password_input.send_keys(self.password)
            print("Password entered Successfully!")
            self.random_sleep()
        except Exception as e:
            print("Failed to enter password")

    def click_sign_in(self):
        try:
            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
            sign_in_button.click()
            print("Sign in Button clicked!")
            self.random_sleep()
        except Exception as e:
            print("Failed to click on sign in button")

    def try_otp_to_sign_in(self):
        try:
            otp_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
            print("Please enter the OTP in the browser...")
            self.wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
            print(f"OTP detected: {otp_input.get_attribute('value')}")
            self.random_sleep()
            
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
            submit_button.click()
            print("Submit button clicked successfully!")
            self.random_sleep()
            
        except Exception as otp_exception:
            print("OTP step skipped or not required.")
    
            
    def close(self):
        print("closing the browser")
        self.driver.quit()

    def login(self):
        try:
            self.open_page()
            self.sign_in_with_email_btn()
            self.enter_email()
            self.enter_password()
            self.click_sign_in()
            self.try_otp_to_sign_in()
            print("login successful") 
            return self.driver
        except Exception as e:
            print("login fail")
            return False         