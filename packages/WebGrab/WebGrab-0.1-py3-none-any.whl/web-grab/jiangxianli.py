from .base_scary import BaseScary
from .httpbin import HttpBin

class JiangXianLi(BaseScary):
    BaseUrl = "https://ip.jiangxianli.com/"
    Rules = {
        "list": [
            {"tag": 'list',"rule": '//div[@class="container"]//div[@class="item"]//a/@href'}
        ],
        "lastBlog": [
            {"tag": 'lastBlog',"rule": '//div[@class="container"]//div[@class="item"][1]//a/@href'}
        ],
        "ips" : [
            {"tag": "ips", "rule": "//div[@class='container']/div[@class='contar-wrap']/div[@class='item']//p/text()"}
        ]
    }
    def blogs(self,method="lastBlog"):
        ''' 
            获取[https://ip.jiangxianli.com]最新的blog's url
            参数： method (list,lastBlog)
            返回： list|string,ErrorMessage
        '''
        self.set_url("{0}/blog.html".format(self.BaseUrl))
        self.set_rules(self.Rules[method])

        blogs_url , err = self.active()

        if err == None:
            urls = []
            for blog in blogs_url:
                if method in blog.keys():
                    urls.append(blog[method])
            if len(urls) > 0:
                return urls[0],None
            return [],None
        else:
            return None, err

    def ips(self,url,limit_area="中国"):
        self.set_url(url)
        self.set_rules(self.Rules["ips"])

        ips_result,err = self.active()
        if err == None:
            ips = []
            for ips_list in ips_result:
                for ip_str in ips_list["ips"]:
                    if ip_str.find(limit_area) > 0:
                        ip = ip_str.split("@",1)[0].strip()
                        schmed = ip_str.split("@",1)[1].split("#",1)[0].strip()
                        ips.append("{0}://{1}".format(schmed,ip).lower())
            return ips,None
        else:
            return None,err

    def valid_ips(self,url,limit_area="中国"):
        ips_arr, err = self.ips(url,limit_area)
        if err != None:
            return None,err
        
        httpbin = HttpBin()
        ips = []
        for ip in ips_arr:
            proxy_status ,_ = httpbin.IsProxyIP(ip)
            if proxy_status:
                ips.append(ip)
        
        return ips,None


