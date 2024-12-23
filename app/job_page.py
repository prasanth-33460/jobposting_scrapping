import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from app.scrap import Scrap

class JobPage:
    def __init__(self,driver,job_url):
        self.driver = driver
        self.browser = driver
        self.job_url = job_url        
        self.wait = WebDriverWait(self.browser, 20)
    
    def random_sleep(self):
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)
        
    def job_page_redirect(self):
        try:
            self.driver.get(self.job_url)
            self.random_sleep()
            print("job page link is opened")
        except Exception as e:
            print("redirecting to job url failed")
            
    def click_on_job_link(self):
        while True:
            try:
                link_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='t-roman t-sans']//a[@href]")))   
                if not link_elements:
                    print("No job links found.")
                    break
                for link in link_elements:
                    link_text = link.text.strip()
                    link_href = link.get_attribute("href")
                    print(f"Clicking on link: {link_text} ({link_href})")
                    self.random_sleep()
                    
                    ActionChains(self.driver).move_to_element(link).perform()
                    link.click()
                    self.random_sleep()            
                print("Link clicked successfully!")
            except Exception as e:
                print(f"Error occurred: {e}")
                break
            
    def view_applicants_btn(self):
        try:
            view_applicants_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'mr2') and .//span[text()='View applicants']]")))
            print("Clicking on 'View applicants' button.")
            view_applicants_button.click()
            self.random_sleep()    
            Scrap.scrap_info()
            self.driver.back()
            self.random_sleep()
        except Exception as e:
            print("was not able to click on view applicants button")
            
    def entering_applicants_page(self):
        try:
            self.job_page_redirect()
            self.click_on_job_link()
            self.view_applicants_btn()
            print("job applicants are now listed!")
            return self.driver
        except Exception as e:
            print("some confused error!")
            return False