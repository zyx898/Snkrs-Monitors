import random
import threading

class Proxy(object):
    def __init__(self, proxy_string=None):
        if proxy_string:
            self.parse_proxy_string(proxy_string)
        else:
            self.proxy_string = None

    def parse_proxy_string(self, proxy_string):
        split_string = proxy_string.strip('\n').split(':')

        self.ip = split_string[0]
        self.port = split_string[1]
        self.proxy_string = '{0}:{1}'.format(self.ip, self.port)

        self.authenticated = len(split_string) == 4
        if self.authenticated:
            self.username = split_string[2]
            self.password = split_string[3]
            self.proxy_string = '{0}:{1}@{2}'.format(self.username, self.password, self.proxy_string)

    def get_dict(self):
        return {
            'http': 'http://{}'.format(self.proxy_string),
            'https': 'https://{}'.format(self.proxy_string)
        } if self.proxy_string else {}

class ProxyManager(object):
    def __init__(self, proxy_file_path=None):
        self.proxies = self.load_proxies_from_file(proxy_file_path) if proxy_file_path else [Proxy()]
        self.lock = threading.Lock()
        self.current_proxy = 0

    @staticmethod
    def load_proxies_from_file(proxy_file_path):
        proxies = []
        with open(proxy_file_path) as proxy_file:
            for proxy_string in proxy_file.readlines():
                proxies.append(Proxy(proxy_string))
        return proxies

    def random_proxy(self):
        return random.choice(self.proxies)

    def next_proxy(self):
        if self.current_proxy >= len(self.proxies):
            self.current_proxy = 0

        with self.lock:
            proxy = self.proxies[self.current_proxy]
            self.current_proxy += 1
            return proxy