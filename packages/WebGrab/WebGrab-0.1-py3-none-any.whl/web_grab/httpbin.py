from .base_scary import BaseScary

class HttpBin(BaseScary):
    BaseUrl = "https://httpbin.org"
    Rules = {
        "ip": [{"tag": 'IP', "rule": "origin", "rules": []}]
    }

    def IsProxyIP(self,proxy_ip):
        ''' 
            验证【代理IP】是否有效
            返回： True|false,ErrorMessage
        '''
        self.set_url("{0}/ip".format(self.BaseUrl))
        self.set_rules(self.Rules["ip"])
        self.set_proxy(proxy_ip)

        result, err = self.active()

        if err == None:
            for ip_origin in result:
                if  (proxy_ip.find(ip_origin["IP"]) >= 0) and (len(ip_origin["IP"].split(".")) == 4):
                    return True,None
        else:
            return None, err

        return False,None