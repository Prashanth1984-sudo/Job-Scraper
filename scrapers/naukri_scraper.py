from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_naukri_jobs(keyword, location, pages=1):
    jobs = []
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    keyword_param = "-".join(keyword.strip().split())
    location_param = "-".join(location.strip().split())

    for page in range(1, pages+1):
        url = f"https://www.naukri.com/{keyword_param}-jobs-in-{location_param}?k={keyword}&l={location}&page={page}"
        driver.get(url)
        time.sleep(2)  # initial wait for page load

        # Close any pop-up tabs automatically opened
        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_window)

        try:
            job_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jobTuple")))
        except:
            continue

        for card in job_cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                company_elem = card.find_element(By.CSS_SELECTOR, "a.subTitle")
                location_elem = card.find_element(By.CSS_SELECTOR, "li.location")
                title = title_elem.text.strip()
                company = company_elem.text.strip()
                location_text = location_elem.text.strip()
                link = title_elem.get_attribute("href")
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "link": link
                })
            except Exception:
                continue

        time.sleep(1)  # small delay to allow next page to load

    driver.quit()
    return jobs
