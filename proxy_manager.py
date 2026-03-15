import random
import threading
import requests
from stem import Signal
from stem.control import Controller
import socks
import socket

class ProxyManager:
    def __init__(self, proxy_list, use_tor=False, tor_port=9050, tor_control_port=9051):
        self.proxy_list = proxy_list
        self.use_tor = use_tor
        self.tor_port = tor_port
        self.tor_control_port = tor_control_port
        self.current_index = 0
        self.lock = threading.Lock()
        self.failed_proxies = set()
        if use_tor:
            self._renew_tor_circuit()

    def _renew_tor_circuit(self):
        try:
            with Controller.from_port(port=self.tor_control_port) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
            print("[Tor] Circuit renewed")
        except Exception as e:
            print(f"[Tor] Error: {e}")

    def get_proxy_dict(self):
        with self.lock:
            if self.use_tor:
                return {'http': f'socks5://127.0.0.1:{self.tor_port}',
                        'https': f'socks5://127.0.0.1:{self.tor_port}'}
            if not self.proxy_list:
                return None
            available = [p for p in self.proxy_list if p not in self.failed_proxies]
            if not available:
                available = self.proxy_list
            proxy = random.choice(available)
            return {'http': proxy, 'https': proxy}

    def mark_failed(self, proxy):
        with self.lock:
            self.failed_proxies.add(proxy)

    def get_requests_session(self):
        session = requests.Session()
        proxy_dict = self.get_proxy_dict()
        if proxy_dict:
            session.proxies.update(proxy_dict)
        return session

    def socks5_socket(self, dest_host, dest_port):
        if self.use_tor:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.tor_port)
        else:
            proxy = self.get_proxy_dict()
            if proxy and 'http' in proxy:
                parts = proxy['http'].replace('socks5://', '').split('@')
                if len(parts) == 2:
                    auth, addr = parts
                    user, passwd = auth.split(':')
                    ip, port = addr.split(':')
                    socks.set_default_proxy(socks.SOCKS5, ip, int(port), True, user, passwd)
                else:
                    ip, port = parts[0].split(':')
                    socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket.socket = socks.socksocket
        return socket.create_connection((dest_host, dest_port))
