import requests,colorama,time
from colorama.ansi import Fore

colorama.init(autoreset=True)

class ProxyController:
    def __init__(self):
        self.__proxysSuccess = []
        self.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

    def proxyControl(self,proxies,url="https://www.google.com",timeout=(3.05,27),details=True):
        """You should send the proxy list you want to check.\n
        proxies  : Proxies parameter must be list or str. (List or String)\n
        url     : Give url to check proxy. (https-http)\n
        timeout : Set a waiting time to connect. Default timeout = (3.05,27) >> (connect,read)\n
        details : Information message about whether the proxy is working or not. (True or False)\n
        User Agent : You can find it by typing my user agent into Google.\n
        Default User Agent : Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"""
        try:
            self.__exceptions(proxies,details,url,timeout)
        except Exception as err :
            return print("Error :: > "+str(err))
        URL = url
        TIMEOUT = timeout
        session = requests.Session()
        session.headers['User-Agent'] = self.userAgent
        session.max_redirects = 300
        finishedMsg = "Proxy check completed."
        if type(proxies) == list:
            for proxy in proxies:
                self.__proxyCheck(proxy, session, URL, TIMEOUT, details)
            print(finishedMsg)
            if len(self.__proxysSuccess) == 0 :
                print("None of the proxies you provided are working.")
            else :
                return self.__proxysSuccess
        elif type(proxies) == str:
            self.__proxyCheck(proxies, session, URL, TIMEOUT, details)
            print(finishedMsg)
            if len(self.__proxysSuccess) == 0 :
                print("Proxy address not working.")
            else :
                return self.__proxysSuccess[0]
        
    def __proxyCheck(self, proxy, session, URL, TIMEOUT, details):
        protocols = ["http","socks4","socks5"]
        if details == True:
            for protocol in protocols:
                try :
                    start = time.time()
                    session.get(URL, proxies={'https':f"{protocol}://{proxy}", "http":f"{protocol}://{proxy}"}, timeout=TIMEOUT,allow_redirects=True)
                    timeOut = (time.time() - start)
                    print(Fore.LIGHTGREEN_EX+"Protocol : %s - Connection Successfull - %s" %(protocol,proxy))
                    self.__proxysSuccess.append(proxy)
                    print(Fore.LIGHTBLUE_EX+self.__proxy_Details(protocol,proxy,timeOut))
                    break
                except :
                    print(Fore.LIGHTRED_EX+"Protocol : %s - The connection is unstable - %s" %(protocol,proxy))
                    continue
        else :
            for protocol in protocols:
                try :
                    session.get(URL, proxies={'https':f"{protocol}://{proxy}", "http":f"{protocol}://{proxy}"}, timeout=TIMEOUT,allow_redirects=True)
                    self.__proxysSuccess.append(proxy)
                except :
                    continue

    def __exceptions(self,proxies,details,url,timeout):
        if type(proxies) != list and type(proxies) != str :
            raise Exception("The proxys parameter must be a list.")
        elif str(url).find("http") == -1:
            raise Exception("The url parameter must be a link.")
        elif type(timeout) == bool or type(timeout) == str :
            raise Exception("The timeout parameter must be tuple, integer or float.")
        elif type(details) != bool:
            raise Exception("The details parameter must be true or false.")
        else :
            pass

    def __proxy_Details(self,protocol,proxy,timeOut):
        getUrl = requests.get("https://ipwhois.app/json/",proxies={'https':f"{protocol}://{proxy}", "http":f"{protocol}://{proxy}"})
        response = getUrl.json()
        ipAddr = response["ip"]
        proxyType = response["type"]
        country = response["country"]
        time_out = timeOut
        text = f"proxyIp : {ipAddr} -- proxyType : {proxyType} -- country : {country} -- timeOut : {time_out:.2f} second"  
        return text