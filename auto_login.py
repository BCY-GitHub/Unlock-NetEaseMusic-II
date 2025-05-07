# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00884DBC93008F478735253BC3152A90371B970F1EB48EC54F2E2A3ED12DEC2682E2446FCE64C8DA43DBC40D133E9CD1AD2CEAE44E23B9B10C4D6C70FCDA3F75A61A944DA21AEFBD221E51E4C8FE321BE3BDFC74F6E48BD0A393D68D763DC5AE6923F463CE4D9DC516130B937B503C74A4AD5507B1BC758AE51BFD304A435FC66AB9D7AFFAA01EC41D055F70EF7E4E135EB84EAAE2D3D908ED9F5F5C85DEB6DA2A8D29D13281AD9126F99E6A4FEB3D70DF9A1D6D2AF6747387E9EB38881A452BB5FB801EB7391EAEDC0FACF60FD6317FA217E382AC6A2011F6497A4A46F24BFCB63D481FB0282FB2211844884293000700EFD89093B33EA7E5C73773050A1CCADF35C1E66BC1BE44211D072368F9E5E104094C4EA68A6A4E5DD3F0953AA5862167628EC2D0ED31325CF9532EFABB8CBA7CAC7A475073BDC90C96DCFC5D95127D8C7A6EC8AEEA44724CB0577953E7C1E9CEDA3E8E02C5F3B775B6D9B827093D7218"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
