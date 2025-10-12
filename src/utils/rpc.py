from src import *
from src.utils.files import files

class RPC:
    def __init__(self):
        try:
            smalltext = f'Tokens » {len(files.gettokens())} Proxies » {len(files.getproxies())}'
            self.clientid = '1426926672976019456'
            self.rpc = Presence(self.clientid)
            self.rpc.set({
                'state': 'discord.gg/spamming',
                'details': 'G4Tools.cc',
                'timestamps': {'start': int(time.time())},
                'assets': {
                    'large_image': 'smalllogorounded',
                    'large_text': 'discord.gg/spamming',
                    'small_image': 'folder',
                    'small_text': smalltext
                },
                'buttons': [
                    {'label': 'Join Discord', 'url': 'https://discord.gg/spamming'},
                    {'label': 'Get G4Spreader for FREE', 'url': 'https://github.com/r3ci/G4Spreader'}
                ]
            })
        except:
            pass

    def update(self, details):
        try:
            smalltext = f'Tokens » {len(files.gettokens())} Proxies » {len(files.getproxies())}'
            self.rpc.set({
                'state': 'Simply the best',
                'details': details,
                'timestamps': {'start': int(time.time())},
                'assets': {
                    'large_image': 'smalllogorounded',
                    'large_text': 'discord.gg/spamming',
                    'small_image': 'folder',
                    'small_text': smalltext
                },
                'buttons': [
                    {'label': 'Join Discord', 'url': 'https://discord.gg/spamming'},
                    {'label': 'Get G4Spreader for FREE', 'url': 'https://github.com/r3ci/G4Spreader'}
                ]
            })
        except:
            pass
RPC = RPC()
