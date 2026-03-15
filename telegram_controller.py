import telebot
import threading
import logging

logger = logging.getLogger('TelegramController')

class TelegramController:
    def __init__(self, token, reporting_engine, whatsapp_harvester, account_creator, db):
        self.bot = telebot.TeleBot(token)
        self.reporting_engine = reporting_engine
        self.whatsapp_harvester = whatsapp_harvester
        self.account_creator = account_creator
        self.db = db
        self._setup_handlers()

    def _setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, "🔥 Rebel System Online. Commands:\n"
                                        "/add_target <platform> <username> - add social media target\n"
                                        "/add_number <phone> - add WhatsApp number\n"
                                        "/status - show current targets\n"
                                        "/create_account <platform> - create new account\n"
                                        "/stats - show statistics")

        @self.bot.message_handler(commands=['add_target'])
        def add_target(message):
            try:
                parts = message.text.split()
                platform = parts[1]
                username = parts[2]
                url = f"https://www.{platform}.com/{username}"
                self.reporting_engine.add_report_task(platform, username, url)
                self.bot.reply_to(message, f"Target {username} added to queue.")
            except:
                self.bot.reply_to(message, "Usage: /add_target <platform> <username>")

        @self.bot.message_handler(commands=['add_number'])
        def add_number(message):
            try:
                number = message.text.split()[1]
                self.whatsapp_harvester.add_target_number(number)
                self.reporting_engine.add_report_task('whatsapp', phone=number)
                self.bot.reply_to(message, f"Number {number} added.")
            except:
                self.bot.reply_to(message, "Usage: /add_number <phone>")

        @self.bot.message_handler(commands=['status'])
        def status(message):
            targets = self.db.get_all_targets()
            msg = "Targets:\n"
            for t in targets[-10:]:
                msg += f"{t[2] or t[4]} ({t[1]}): {t[5]} reports\n"
            self.bot.reply_to(message, msg)

        @self.bot.message_handler(commands=['create_account'])
        def create_account(message):
            try:
                platform = message.text.split()[1]
                if platform == 'facebook':
                    cred = self.account_creator.create_facebook_account()
                    if cred:
                        self.bot.reply_to(message, f"Created {platform} account: {cred['email']}:{cred['password']}")
                    else:
                        self.bot.reply_to(message, "Account creation failed.")
                else:
                    self.bot.reply_to(message, "Platform not supported.")
            except:
                self.bot.reply_to(message, "Usage: /create_account <platform>")

        @self.bot.message_handler(commands=['stats'])
        def stats(message):
            self.bot.reply_to(message, "Stats placeholder.")

    def start(self):
        threading.Thread(target=self.bot.polling, daemon=True).start()
        logger.info("Telegram controller started")
