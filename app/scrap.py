import os
import random 
import time 
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait

class Scrap:
    def __init__(self,driver, output_dir='output', output_file='scraping_output.csv'):
        self.driver = driver
        self.browser = driver
        self.wait = WebDriverWait(self.browser,20)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        self.output_path = os.path.join(output_dir, output_file)

        if not os.path.exists(self.output_path):
            with open(self.output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Applicant Name', 'Location', 'Email', 'Phone Number'])
                
    def random_sleep(self):
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)
                
    def go_to_next_page(self):
        try:
            pagination_buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'artdeco-pagination__indicator--number')]//button")))
            active_page = self.driver.find_element(By.XPATH, "//li[contains(@class, 'active')]//button")
            active_page_number = int(active_page.text.strip())  
            total_pages = len(pagination_buttons)
            if active_page_number == total_pages:
                print("Reached the last page. Stopping the scraping process.")
                return
            
            for button in pagination_buttons:
                page_number = int(button.text.strip())
                if page_number > active_page_number: 
                    button.click()
                    self.random_sleep()  
                    print(f"Moved to page {page_number}")
                    break
            self.scrap_info()
        except Exception as e:
            print(f"Error occurred while navigating to next page: {e}") 
            
    def scrap_info(self):
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_sleep()
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
            applicants = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'hiring-applicants__list-item')]//a")))
            if not applicants:
                print("No applicants found on this page.")
                return
            is_last_page = len(applicants) < 25
            
            with open(self.output_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                for index, applicant in enumerate(applicants, start=1):
                    try:
                        self.random_sleep()
                        applicant.click()
                        
                        name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'hiring-applicant-header')]//h1"))).text
                        applicant_name = name.split("’s application")[0] 
                        location = self.driver.find_element(By.XPATH, "//*[contains(@class, 'hiring-applicant-header')]//div[contains(@class, 't-16')][2]").text
                        
                        more_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'hiring-applicant-header-actions')]//button[contains(@class, 'artdeco-dropdown__trigger')]//span[text()='More…']")))
                        more_button.click()
                        
                        email = None
                        try:
                            email_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[a[contains(@href, 'mailto:')]]//span[@class='hiring-applicant-header-actions__more-content-dropdown-item-text' and @aria-hidden='true']")))
                            email = email_element.text.strip()
                        except:
                            email = "Not Available"
                        
                        phone_number = None
                        try:
                            phone_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[div[contains(@class, 'artdeco-dropdown__item')]]//span[contains(@class, 'hiring-applicant-header-actions__more-content-dropdown-item-text')]")))
                            phone_number = phone_element.text.strip()
                        except:
                            phone_number = "Not Available"  
                        
                        writer.writerow([applicant_name, location, email, phone_number])

                        print(f"Applicant Number {index}:")
                        print(f"Name: {applicant_name}")
                        print(f"Location: {location}")
                        print(f"Email: {email}")
                        print(f"Phone Number: {phone_number}")
                        print("-" * 40)
                    
                        self.random_sleep()
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        
            if is_last_page:
                print("Reached the last page with less than 25 applicants. Stopping the scraping process.")
                return
            self.go_to_next_page()
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def scrap_logic(self):
        self.scrap_info()