from src import *
from src.utils.files import files
from src.cli import dashboard, logger
tokendata = {}


# removed the good stuff so the skids dont skid lol
class responsewrapper:
    def __init__(self, response=None, error=None):
        if response:
            self._response = response
            self.status_code = response.status_code
            self.headers = dict(response.headers) if response.headers else {}
            self.text = response.text
            self.cookies = response.cookies
            self.error = None
        else:
            self._response = None
            self.status_code = 0
            self.headers = {}
            self.text = str(error) if error else 'Error'
            self.cookies = None
            self.error = error
    
    def json(self) -> dict:
        if self.error:
            return {}
            
        try:
            return self._response.json()
        
        except Exception as e:
            return {}

# removed the good stuff so the skids dont skid lol
class sessionwrapper:
    def __init__(self, impersonate=None):
        self.session = curlcffi.Session(
            impersonate=impersonate,
            timeout=15
        )
        self.cookies = self.session.cookies
        self.headers = dict(self.session.headers) if self.session.headers else {}
    
    @property
    def proxies(self):
        return self.session.proxies

    @proxies.setter
    def proxies(self, val):
        self.session.proxies = val
        
    def adddata(self, kwargs):
        headers = kwargs.get('headers', {})
        if 'json' in kwargs:
            payload = kwargs.pop('json')
            jsonstr = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
            kwargs['data'] = jsonstr.encode('utf-8')
            headers['Content-Type'] = 'application/json; charset=utf-8'

        elif 'data' in kwargs and kwargs['data'] is not None:
            data = kwargs['data']
            if isinstance(data, str):
                kwargs['data'] = data.encode('utf-8')

        if headers:
            kwargs['headers'] = headers
        return kwargs
   
    def request(self, method, url, **kwargs):
        headers = dict(kwargs.get('headers', {})) if kwargs.get('headers') else {}
        kwargs['headers'] = headers
        kwargs = self.adddata(kwargs)
        r = self.session.request(method, url, **kwargs)
        return responsewrapper(r)
            
    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)
    
    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)
   
    def patch(self, url, **kwargs):
        return self.request('PATCH', url, **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

# removed the good stuff so the skids dont skid lol
class curlwrapper:
    def Session(impersonate=None):
        return sessionwrapper(impersonate=impersonate)

# removed the good stuff so the skids dont skid lol
class apibypassing_:
    def __init__(self):
        logger.info('Initializing API bypassing')
        self.cffiversion = 'chrome136'

        self.headers = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua-platform': '"Windows"',
            'authorization': None,
            'x-debug-options': 'bugReporterEnabled',
            'sec-ch-ua': f'"Google Chrome";v="140", "Chromium";v="140", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'x-discord-timezone': 'Europe/Warsaw',
            'x-super-properties': None,
            'x-discord-locale': 'en-US',
            'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i'
        }

    def getcookie(self, headers):
        r = requests.get('https://discord.com', headers=headers)
        r.cookies.set('locale', 'en-GB', domain='.discord.com', path='/')
        return r.cookies, '; '.join([f'{cookie.name}={cookie.value}' for cookie in r.cookies])
apibypassing = apibypassing_()

# removed the good stuff so the skids dont skid lol
class client:
    def __init__(self, token=None, referrer='https://discord.com/channels/@me'):
        self.token = token
        self.proxy = None
        self.fullproxy = None
        self.maskedtoken = token[:30] if token else None

        self.cookiejar = tokendata[token]['cookiejar']
        self.cookiestr = tokendata[token]['cookiestr']

        self.sess = self.makesess()
        self.chooseproxy()
        if files.getproxies():
            self.setproxy()

        self.headers = copy.deepcopy(apibypassing.headers)
        self.settoken(token)
        # yes ik this cause of skidssssssss
        self.addxsup('eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE0MS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTQxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5wcml2YWN5d2FsbC5vcmcvIiwicmVmZXJyaW5nX2RvbWFpbiI6Ind3dy5wcml2YWN5d2FsbC5vcmciLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6NDU3MTc0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJjbGllbnRfbGF1bmNoX2lkIjoiYzY4ZmMyODYtYTdjNC00YTFhLWIxOWMtNmVlNzI3ODY0NDkwIiwibGF1bmNoX3NpZ25hdHVyZSI6IjgyNDMwMTBiLTcwYTktNDE1MC05Yjc2LTdlYjNhOGE1NjVmMiIsImNsaWVudF9oZWFydGJlYXRfc2Vzc2lvbl9pZCI6IjhjYTk2N2U2LTFjNTQtNDMwZi04YzE0LTA2MjU5YTRkYTJiOSIsImNsaWVudF9hcHBfc3RhdGUiOiJmb2N1c2VkIn0=')

    def makesess(self):
        return curlwrapper.Session(impersonate=apibypassing.cffiversion)

    def refreshcookies(self):
        self.cookiejar, self.cookiestr = apibypassing.getcookie(self.headers)
        self.updatecookies(self.cookiejar, self.cookiestr)
        tokendata[self.token]['cookiejar'] = self.cookiejar
        tokendata[self.token]['cookiestr'] = self.cookiestr

    def updatecookies(self, cookiejar, cookiestr):
        if not self.cookiejar:
            self.cookiejar, self.cookiestr = apibypassing.getcookie(self.headers)
            
        self.headers['cookie'] = cookiestr
        self.sess.cookies.update(cookiejar)
        tokendata[self.token]['cookiejar'] = self.cookiejar
        tokendata[self.token]['cookiestr'] = self.cookiestr

    def chooseproxy(self):
        try:
            proxylist = files.getproxies()
            if proxylist:
                self.proxy = random.choice(proxylist)
                self.fullproxy = f'http://{self.proxy}'

            else:
                self.proxy = None
                self.fullproxy = None
                
        except:
            self.proxy = None
            self.fullproxy = None

    def setproxy(self):
        if self.fullproxy:
            self.sess.proxies = {
                'http': self.fullproxy,
                'https': self.fullproxy
            }

    def settoken(self, token):
        if token:
            self.headers['authorization'] = token

    def addxsup(self, xsuper):
        self.headers['x-super-properties'] = xsuper

# removed the good stuff so the skids dont skid lol
logger.info('Fetching discord related stuff')
for token in files.gettokens():
    tokendata[token] = {
        'cookiejar': None,
        'cookiestr': None
    }