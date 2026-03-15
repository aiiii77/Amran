import time
import random
import threading
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import RebelBrowser

logger = logging.getLogger('ReportingEngine')

class ReportingEngine:
    def __init__(self, db, proxy_manager, config):
        self.db = db
        self.proxy_manager = proxy_manager
        self.config = config
        self.task_queue = []
        self.queue_lock = threading.Lock()
        self.running = True
        self.workers = []

    def start_workers(self):
        for i in range(self.config.MAX_THREADS):
            t = threading.Thread(target=self._worker_loop)
            t.daemon = True
            t.start()
            self.workers.append(t)
        logger.info(f"Started {self.config.MAX_THREADS} reporting workers")

    def _worker_loop(self):
        while self.running:
            task = self._get_task()
            if task:
                self._execute_report(task)
            else:
                time.sleep(2)

    def _get_task(self):
        with self.queue_lock:
            if self.task_queue:
                return self.task_queue.pop(0)
        return None

    def add_report_task(self, platform, username=None, url=None, phone=None):
        target_id = self.db.add_target(platform, username, url, phone)
        with self.queue_lock:
            self.task_queue.append({
                'id': target_id,
                'platform': platform,
                'username': username,
                'url': url,
                'phone': phone
            })
        logger.info(f"Added report task for {platform}/{username or phone}")

    def _execute_report(self, task):
        platform = task['platform']
        target_id = task['id']
        target_username = task['username']
        target_url = task['url']
        target_phone = task['phone']

        creds = self.db.get_unused_credentials(platform, limit=5)
        if not creds:
            logger.warning(f"No credentials for {platform}, skipping report")
            return

        for cred in creds:
            cred_id, email, password, phone, cookies = cred
            try:
                proxy = self.proxy_manager.get_proxy_dict()
                browser = RebelBrowser(headless=self.config.BROWSER_HEADLESS, proxy=proxy)
                driver = browser.start()
                if not driver:
                    continue

                success = False
                if platform == 'facebook':
                    success = self._report_facebook(driver, email, password, target_url)
                elif platform == 'tiktok':
                    success = self._report_tiktok(driver, email, password, target_url)
                elif platform == 'instagram':
                    success = self._report_instagram(driver, email, password, target_url)
                elif platform == 'twitter':
                    success = self._report_twitter(driver, email, password, target_url)
                elif platform == 'whatsapp':
                    success = self._report_whatsapp(driver, email, password, target_phone)
                else:
                    success = False

                browser.quit()

                if success:
                    self.db.increment_reports(target_id)
                    self.db.mark_credential_used(cred_id)
                    logger.info(f"Report sent using {email or phone} on {platform}")
                    break
                else:
                    logger.debug(f"Report failed with {email or phone}")

            except Exception as e:
                logger.error(f"Reporting exception: {e}")
                if 'driver' in locals():
                    browser.quit()

    def _report_facebook(self, driver, email, password, target_url):
        try:
            driver.get('https://www.facebook.com/')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
            driver.find_element(By.ID, "email").send_keys(email)
            driver.find_element(By.ID, "pass").send_keys(password)
            driver.find_element(By.NAME, "login").click()
            time.sleep(5)
            driver.get(target_url)
            time.sleep(3)
            menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='More' or @aria-label='Account' or contains(@class,'x1i10hfl')]"))
            )
            menu.click()
            time.sleep(1)
            report = driver.find_element(By.XPATH, "//span[contains(text(),'Find support or report')]")
            report.click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//span[contains(text(),'Harassment')]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]").click()
            time.sleep(2)
            return True
        except:
            return False

    def _report_tiktok(self, driver, email, password, target_url):
        try:
            driver.get('https://www.tiktok.com/login')
            time.sleep(3)
            driver.find_element(By.XPATH, "//div[contains(text(),'Use phone / email')]").click()
            time.sleep(1)
            driver.find_element(By.NAME, 'username').send_keys(email)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]").click()
            time.sleep(5)
            driver.get(target_url)
            time.sleep(3)
            share_btn = driver.find_element(By.XPATH, "//button[@data-e2e='share-button']")
            share_btn.click()
            time.sleep(1)
            report_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Report')]")
            report_btn.click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//span[contains(text(),'Harassment')]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
            time.sleep(2)
            return True
        except:
            return False

    def _report_instagram(self, driver, email, password, target_url):
        # Placeholder – implement similarly
        return False

    def _report_twitter(self, driver, email, password, target_url):
        # Placeholder
        return False

    def _report_whatsapp(self, driver, email, password, target_phone):
        # Placeholder
        return False

    def stop(self):
        self.running = False
