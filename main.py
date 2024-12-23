from fastapi import FastAPI
from app.login import LoginModule
from app.job_page import JobPage
from app.scrap import Scrap

app = FastAPI()

@app.get('/')
def scrap_applicants():
    base_url = 'https://www.linkedin.com/'
    job_url = 'https://www.linkedin.com/my-items/posted-jobs/'
    mail = 'prasanth33460@gmail.com'
    password = ''
    try:
        login_module = LoginModule(base_url,mail,password)
        driver = login_module.login()
        if not driver:
            print("login failed")
        else:
            print("login success")
        
        job_page = JobPage(driver,job_url)
        print("redirecting to job post page...")
        job_page.entering_applicants_page()
        
        applicant_scrap = Scrap(driver)
        print("now scrapping applicants!")
        applicant_scrap.scrap_logic()
    except Exception as e:
        print("ERROR 404")
    finally:
        if driver:
            driver.quit()
            print("browser closed")
        login_module.close()
