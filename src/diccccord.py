from src import *
from src.cli import dashboard, logger
from src.utils.sessionmanager import *
from src.utils.stats import Stats

class disccccord:
    def __init__(self, token, config, stats, setstatsfuncclass):
        self.client = client(token)
        self.token = token
        self.opendms = config['opendms']
        self.servers = config['servers']
        self.message = config['message']
        self.stats: Stats = stats
        self.setstatsfuncclass: dashboard = setstatsfuncclass
    
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

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return [], True

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return [], True

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

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return [], True

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return [], True
        
    def getchannels(self, serverid):
        channels = []
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

            while True:
                r = self.client.sess.get(
                    f'https://discord.com/api/v9/guilds/{serverid}/channels',
                    headers=self.client.headers
                )

                if r.status_code == 200:
                    for channel in r.json():
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

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return [], True

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return [], True
        
    def send(self, channelid):
        try:
            if not self.client.cookiejar:
                logger.info(f'{self.client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

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

            else:
                logger.error(f'{self.client.maskedtoken} » {r.text}')
                if '50001' in r.text or '340013' in r.text:
                    return False
                return True

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
                self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, percent=self.stats.progress())
        
        if self.servers:
            servers,end = self.getservers()
            if end:
                return
            
            for server in servers:
                channels, end = self.getchannels(server)
                if end:
                    return
                else:
                    self.stats.totaltosend += len(channels)
                    serverchannelids.extend(channels)
                    self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, percent=self.stats.progress())
        
        for dm in opendmids:
            end = self.send(dm)
            if end:
                return
            else:
                self.stats.toopendms += 1
                self.stats.totalsent += 1
                self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, percent=self.stats.progress())

        for channel in serverchannelids:
            end = self.send(channel)
            if end:
                return
            else:
                self.stats.totalsent += 1
                self.setstatsfuncclass.setstats(sentdms=self.stats.toopendms, sentchannels=self.stats.toopenchannels, percent=self.stats.progress())