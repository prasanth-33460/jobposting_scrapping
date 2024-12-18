import random 
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains

def random_sleep():
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)
    
def go_to_next_page():
    try:
        pagination_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'artdeco-pagination__indicator--number')]//button")))
        
        active_page = driver.find_element(By.XPATH, "//li[contains(@class, 'active')]//button")
        active_page_number = int(active_page.text.strip())  
        total_pages = len(pagination_buttons)
        
        if active_page_number == total_pages:
            print("Reached the last page. Stopping the scraping process.")
            return
        
        for button in pagination_buttons:
            page_number = int(button.text.strip())
            if page_number > active_page_number: 
                button.click()
                random_sleep()  
                print(f"Moved to page {page_number}")
                break
        scrap_info()

    except Exception as e:
        print(f"Error occurred while navigating to next page: {e}") 
        
def scrap_info():
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            random_sleep()
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height
        
        applicants = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'hiring-applicants__list-item')]//a")))
        
        if not applicants:
            print("No applicants found on this page.")
            return
        
        is_last_page = len(applicants) < 25
        for index, applicant in enumerate(applicants, start=1):
            try:
                random_sleep()
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
            
                random_sleep()
                
            except Exception as e:
                print(f"An error occurred: {e}")
                
        if is_last_page:
            print("Reached the last page with less than 25 applicants. Stopping the scraping process.")
            return
                
        go_to_next_page()

    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    
driver = webdriver.Chrome()
wait = WebDriverWait(driver,20)
driver.maximize_window()

driver.get('https://www.linkedin.com/')
random_sleep()

sign_in_with_email_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
sign_in_with_email_button.click()
print("Button clicked successfully!")
random_sleep()

email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
email_input.send_keys('prasanth33460@gmail.com')
print("Email entered Successfully!")
random_sleep()

password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
password_input.send_keys('prasanthXbezos@1234509876')
print("Password entered Successfully!")
random_sleep()

sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
sign_in_button.click()
print("Sign in Button clicked!")
random_sleep()

try:
    otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
    print("Please enter the OTP in the browser...")
    wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
    print(f"OTP detected: {otp_input.get_attribute('value')}")
    random_sleep()
    
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
    submit_button.click()
    print("Submit button clicked successfully!")
    random_sleep()
    
except Exception as otp_exception:
    print("OTP step skipped or not required.")
    

job_url = 'https://www.linkedin.com/my-items/posted-jobs/'
driver.get(job_url)

while True:
    try:
        link_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='t-roman t-sans']//a[@href]")))
        
        if not link_elements:
            print("No job links found.")
            break

        for link in link_elements:
            link_text = link.text.strip()
            link_href = link.get_attribute("href")
            print(f"Clicking on link: {link_text} ({link_href})")
            
            random_sleep()
            ActionChains(driver).move_to_element(link).perform()
            link.click()
            random_sleep()
            
        print("Link clicked successfully!")
        
        view_applicants_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'mr2') and .//span[text()='View applicants']]")))
        print("Clicking on 'View applicants' button.")
        view_applicants_button.click()
        random_sleep()
        
        scrap_info()
        driver.back()
        random_sleep()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        break