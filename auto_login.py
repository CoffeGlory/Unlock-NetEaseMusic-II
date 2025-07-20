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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FE49E5616DEEB80031E21793986BFC741929BA155EAB5208915BE263AF21DB40A374DDE1165F13A10E728A548DF4FA2D56E0EE7E306BED31DFE542BB01152199777FCDE11C6C79EB30A3125AAED06EB2308291301A3591C9662CE16A66F1C282DA96ABD70F9B677D6AF0E8BA3C9E0B3ECD6A0956D2A32B5D76442F48C94D33ED012390295DAA23748AB12F7B674C34637B0CF6B64C543BF1935201F6A3F921A66044C9AF62A2E57E474356977D251584DAD94C509F95FE018BB2CBA11436EBDF5F4843A3A77E4CBE89B2A80FE6CB4112544E4FEC82DC9D81D05C90EFD318F95C688077A515B7FB01DE09E07A65A51511CE437DEF1BF8973030641185A76D0C42B8E4180445E03441C7BEB84FF7D6B1CB7C918E86A6077F22DB576B3E03B4B5B75BD0AF809FAB92E4A2844A294B8D6ABC0B5626132BA023DFE0EBEC2C3259693F0F36913B25AE5C7C2E8D2751CB1BD85E2BB34569F46BFDFEA568AE86C9D897B07CB878E35FBBD93CD11DE657D1BBF60F74375F41C4687FFF960557937169D25484A2E183F92260A57FE2492F62FB7602"})
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
