from src import *
from src.cli import dashboard, logger
from src.utils.sessionmanager import *
from src.utils.stats import Stats

class disccccord:
    def __init__(self, token, config, stats, setstatsfuncclass):
        self.client = client(token)
        self.token = token
        self.userid = self.getuserid()
        self.opendms = config['opendms']
        self.servers = config['servers']
        self.message = config['message']
        self.stats: Stats = stats
        self.setstatsfuncclass: dashboard = setstatsfuncclass
    
    def getuserid(self):
        try:
            token = self.token
            tokenparts = token.split('.')
            if len(tokenparts) < 2: return None
            userid = base64.b64decode(tokenparts[0] + '==').decode('utf-8')
            return userid
        except:
            return None

    def hassendpermission(self, channeldata, serverid, memberdata):
        SENDMESSAGES = 0x800
        VIEWCHANNEL = 0x400
        ADMINISTRATOR = 0x8
        
        userroles = memberdata.get('roles', [])
        guildperms = int(memberdata.get('permissions', '0'))
        
        if guildperms & ADMINISTRATOR:
            return True
        
        baseallow = guildperms
        allow = 0
        deny = 0
        
        overwrites = channeldata.get('permission_overwrites', [])
        
        for ow in overwrites:
            if ow['id'] == serverid:
                allow |= int(ow.get('allow', '0'))
                deny |= int(ow.get('deny', '0'))
                break
        
        for ow in overwrites:
            if ow['type'] == 0 and ow['id'] in userroles:
                allow |= int(ow.get('allow', '0'))
                deny |= int(ow.get('deny', '0'))
        
        for ow in overwrites:
            if ow['type'] == 1 and ow['id'] == self.userid:
                allow |= int(ow.get('allow', '0'))
                deny |= int(ow.get('deny', '0'))
                break
        
        permissions = (baseallow & ~deny) | allow
        return (permissions & VIEWCHANNEL) and (permissions & SENDMESSAGES)

    def getopendms(self):
        dms = []
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

            while True:
                r = self.client.sess.get(
                    'https://discord.com/api/v9/users/@me/channels',
                    headers=self.client.headers
                )

                if r.status_code == 200:
                    for dm in r.json():
                        dms.append(dm['id'])
                    logger.success(f'{self.client.maskedtoken} » Got DMS ({len(dms)})')
                    return dms, False

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 1.5)
                    logger.ratelimit(f'{self.client.maskedtoken} » {ratelimit}s')
                    time.sleep(float(ratelimit))

                elif 'Try again later' in r.text:
                    logger.ratelimit(f'{self.client.maskedtoken} » 5s')
                    time.sleep(5)

                elif 'Cloudflare' in r.text:
                    logger.cloudflare(f'{self.client.maskedtoken} » 10s')
                    time.sleep(10)

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return [], True
                
                elif '401' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Dead token')
                    return True

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return [], False

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return [], False

    def getservers(self):
        servers = []
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

            while True:
                r = self.client.sess.get(
                    'https://discord.com/api/v9/users/@me/guilds',
                    headers=self.client.headers
                )

                if r.status_code == 200:
                    for server in r.json():
                        servers.append(server['id'])
                    logger.success(f'{self.client.maskedtoken} » Got servers ({len(servers)})')
                    return servers, False

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 1.5)
                    logger.ratelimit(f'{self.client.maskedtoken} » {ratelimit}s')
                    time.sleep(float(ratelimit))

                elif 'Try again later' in r.text:
                    logger.ratelimit(f'{self.client.maskedtoken} » 5s')
                    time.sleep(5)

                elif 'Cloudflare' in r.text:
                    logger.cloudflare(f'{self.client.maskedtoken} » 10s')
                    time.sleep(10)

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return [], True

                elif '401' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Dead token')
                    return True

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return [], False

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return [], False

    def getmemberdata(self, serverid):
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

            while True:
                r = self.client.sess.get(
                    f'https://discord.com/api/v9/users/@me/guilds/{serverid}/member',
                    headers=self.client.headers
                )
                
                if r.status_code == 200:
                    memberdata = r.json()
                    logger.success(f'{self.client.maskedtoken} » Got member data for {serverid}')
                    return memberdata, False

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 1.5)
                    logger.ratelimit(f'{self.client.maskedtoken} » {ratelimit}s (yes i know huge ratelimits but still faster than other methods)')
                    time.sleep(float(ratelimit))
                    continue

                elif 'Try again later' in r.text:
                    logger.ratelimit(f'{self.client.maskedtoken} » 5s (yes i know huge ratelimits but still faster than other methods)')
                    time.sleep(5)
                    continue

                elif 'Cloudflare' in r.text:
                    logger.cloudflare(f'{self.client.maskedtoken} » 10s (yes i know huge ratelimits but still faster than other methods)')
                    time.sleep(10)
                    continue

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return {}, True
                
                elif '401' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Dead token')
                    return {}, True
                
                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return {}, True

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return {}, True
        
    def getchannels(self, serverid):
        channels = []
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)
            
            if not self.userid:
                logger.error(f'{self.client.maskedtoken} » Failed to get user ID')
                return [], False
            

            memberdata, end = self.getmemberdata(serverid)
            if end:
                return [], False
            
            while True:
                r = self.client.sess.get(
                    f'https://discord.com/api/v9/guilds/{serverid}/channels',
                    headers=self.client.headers
                )
                
                if r.status_code == 200:
                    for channel in r.json():
                        if channel['type'] == 0:
                            if self.hassendpermission(channel, serverid, memberdata):
                                channels.append(channel['id'])

                    logger.success(f'{self.client.maskedtoken} » Got channels for {serverid} ({len(channels)})')
                    return channels, False
                
                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 1.5)
                    logger.ratelimit(f'{self.client.maskedtoken} » {ratelimit}s')
                    time.sleep(float(ratelimit))

                elif 'Try again later' in r.text:
                    logger.ratelimit(f'{self.client.maskedtoken} » 5s')
                    time.sleep(5)

                elif 'Cloudflare' in r.text:
                    logger.cloudflare(f'{self.client.maskedtoken} » 10s')
                    time.sleep(10)

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return [], True
                
                elif '401' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Dead token')
                    return True
                
                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return [], False
                
        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return [], False
        
    def send(self, channelid):
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

            while True:
                r = self.client.sess.post(
                    f'https://discord.com/api/v9/channels/{channelid}/messages',
                    headers=self.client.headers,
                    json={
                        'mobile_network_type': 'unknown',
                        'content': self.message,
                        'flags': 0
                    }
                )

                if r.status_code == 200:
                    logger.success(f'{self.client.maskedtoken} » Sent')
                    self.stats.toopendms += 1
                    self.stats.totalsent += 1
                    self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, totaltosend=self.stats.totaltosend, percent=self.stats.progress())
                    return False

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 1.5)
                    logger.ratelimit(f'{self.client.maskedtoken} » {ratelimit}s')
                    time.sleep(float(ratelimit))

                elif 'Try again later' in r.text:
                    logger.ratelimit(f'{self.client.maskedtoken} » 5s')
                    time.sleep(5)

                elif 'Cloudflare' in r.text:
                    logger.cloudflare(f'{self.client.maskedtoken} » 10s')
                    time.sleep(10)

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return True
                
                elif 'captcha_key' in r.text:
                    logger.captcha(f'{self.client.maskedtoken} Human verification required')
                    return True


                elif '401' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Dead token')
                    return True

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return False

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return True

    def do(self):
        opendmids = []
        serverchannelids = []
        if self.opendms:
            channels, end = self.getopendms()
            if end: 
                return
            else: 
                self.stats.totaltosend += len(channels)
                opendmids.extend(channels)
                self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, totaltosend=self.stats.totaltosend, percent=self.stats.progress())
        
        if self.servers:
            servers, end = self.getservers()
            if end:
                return
            
            for server in servers:
                channels, end = self.getchannels(server)
                if end:
                    return
                else:
                    self.stats.totaltosend += len(channels)
                    serverchannelids.extend(channels)
                    self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, totaltosend=self.stats.totaltosend, percent=self.stats.progress())
        
        for dm in opendmids:
            end = self.send(dm)
            if end:
                return

        for channel in serverchannelids:
            end = self.send(channel)
            if end:
                return
