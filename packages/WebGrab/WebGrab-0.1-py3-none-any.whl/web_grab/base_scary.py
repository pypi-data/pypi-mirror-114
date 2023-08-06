import requests
from .resolu import ResoluJsons, ResoluHtmls
import warnings
warnings.filterwarnings("ignore")

class BaseScary:
    rules = []
    proxies = []
    cookies = ""
    url = ""
    encoding = "utf-8"
    timeout = 5
    def __init__(self, url = "", rules=[], encoding="utf-8",proxies=[],cookies = "",timeout= 5):
        if url.find("http") >= 0:
            self.url = url
        if len(rules) > 0:
            self.rules = rules
        if encoding:
            self.encoding = encoding
        if proxies:
            self.proxies = {}
        if cookies:
            self.cookies = cookies
        self.timeout = timeout

    def set_url(self, url):
        self.url = url

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_rules(self, rules):
        self.rules = rules

    def set_cookies(self, cookies):
        self.cookies = cookies

    def set_proxy(self,proxyIP):
        self.proxies = {"http": proxyIP, "https": proxyIP}

    def _get_headers(self):
        return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def _get_proxies(self):
        return self.proxies

    def _get_cookies(self):
        cooky = {}
        if self.cookies.find(";") > 1:
            for lies in self.cookies.split(';'):
                key,word = lies.split('=',1)
                cooky[key] = word
        return cooky

    def _active_url(self):
        headers = self._get_headers()
        proxies = self._get_proxies()
        cookies = self._get_cookies()
        i = 0
        errMsg = None
        while i < 3:
            try:
                with requests.Session() as s:
                    if len(proxies):
                        response = s.get(self.url, timeout=self.timeout,verify=False,cookies=cookies, proxies=proxies, headers=headers)
                    else:
                        response = s.get(self.url, timeout=self.timeout,cookies=cookies, headers=headers)
                    return response,None
            except requests.exceptions.RequestException as err:
                i += 1
                errMsg = err
                if len(proxies):
                    print("第{0}次请求【{1}】代理【{3}】，异常信息{2}".format(i,self.url,err,proxies))
                else:
                    print("第{0}次请求【{1}】，异常信息{2}".format(i,self.url,err))
        return None,  errMsg

    def _get_response(self):
        response,err = self._active_url()
        if err == None:
            if response.status_code >= 400:
                print(response)
                return None,  SystemExit("请求状态异常")
            response.encoding = self.encoding
            content_type = response.headers["Content-Type"]
            if content_type.find("json") > 0:
                return ResoluJsons(response.json(), self.rules)
            elif content_type.find("html") > 0:
                return ResoluHtmls(response.text, self.rules)
        return None, err

    def active(self):
        response, err = self._get_response()
        return response, err