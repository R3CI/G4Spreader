from src import *
from src.utils.logging import logger
from src.utils.sessionmanager import *

class disccccord:
    def __init__(self, token, config):
        self.client = client(token)
        self.token = token
        self.opendms = config['opendms']
        self.servers = config['servers']
        self.message = config['message']
    
    def getopendms(self):
        dms = []
        try:
            if not self.client.cookiejar:
                logger.infolog(f'{self.client.maskedtoken} » Getting cookies')
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
                    return dms

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

                elif 'captcha_key' in r.text:
                    logger.captcha(f'{self.client.maskedtoken} » Human verification required')

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return []

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return []

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return []

    def getservers(self):
        servers = []
        try:
            if not self.client.cookiejar:
                logger.infolog(f'{self.client.maskedtoken} » Getting cookies')
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
                    return servers

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

                elif 'captcha_key' in r.text:
                    logger.captcha(f'{self.client.maskedtoken} » Human verification required')

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return []

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return []

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return []
        
    def getchannels(self, serverid):
        channels = []
        try:
            if not self.client.cookiejar:
                logger.infolog(f'{self.client.maskedtoken} » Getting cookies')
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
                    return channels

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

                elif 'captcha_key' in r.text:
                    logger.captcha(f'{self.client.maskedtoken} » Human verification required')

                elif 'You need to verify' in r.text:
                    logger.locked(f'{self.client.maskedtoken} Locked/Flagged')
                    return []

                else:
                    logger.error(f'{self.client.maskedtoken} » {r.text}')
                    return []

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')
            return []
        
    def send(self, channelid):
        try:
            if not self.client.cookiejar:
                logger.infolog(f'{client.maskedtoken} » Getting cookies')
                self.client.refreshcookies()
                self.client.updatecookies(self.client.cookiejar, self.client.cookiestr)

            r = self.client.sess.post(
                f'https://discord.com/api/v9/channels/{channelid}/messages',
                headers=client.headers,
                json={
                    'mobile_network_type': 'unknown',
                    'content': self.message,
                    'flags': 0
                }
            )

            if r.status_code == 200:
                logger.success(f'{client.maskedtoken} » Sent')
                return False

            elif 'retry_after' in r.text:
                ratelimit = r.json().get('retry_after', 1.5)
                logger.ratelimit(f'{client.maskedtoken} » {ratelimit}s')
                time.sleep(float(ratelimit))

            elif 'Try again later' in r.text:
                logger.ratelimit(f'{client.maskedtoken} » 5s')
                time.sleep(5)

            elif 'Cloudflare' in r.text:
                logger.cloudflare(f'{client.maskedtoken} » 10s')
                time.sleep(10)

            elif 'You need to verify' in r.text:
                logger.locked(f'{client.maskedtoken} Locked/Flagged')
                return True

            else:
                logger.error(f'{client.maskedtoken} » {e}')
                if ['50001', '340013'] in r.text:
                    return False
                return True

        except Exception as e:
            logger.error(f'{self.client.maskedtoken} » {e}')

    def do(self):
        all = []
        if self.opendms:
            all.append(self.getopendms())
        
        if self.servers:
            servers = self.getservers()
            for server in servers:
                all.append(self.getchannels(server))
        
        for channel in all:
            if self.send(channel):
                return