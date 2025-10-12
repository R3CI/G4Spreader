import sys, os; sys.dont_write_bytecode = True; os.environ['PYTHONDONTWRITEBYTECODE'] = '1'; os.system('cls'); os.system('title G4Spreader - launching...')
from src import *
from src.utils.console import console
from src.cli import dashboard, logger
from src.diccccord import disccccord
from src.utils.files import files
from src.utils.stats import stats


webbrowser.open('https://g4tools.cc')
webbrowser.open('https://discord.gg/spamming')
os.system('title G4Spreader - launching...')
print('Please give it a second to start up it might be blank for 5-15 seconds')
time.sleep(3)

class Dashboard(dashboard):
    def on_mount(self):
        super().on_mount()
        
        logger.logwidget = self.logwidget
        logger.info('Starting up...')
        console.title('G4Spreader - g4tools.cc - discord.gg/spamming - Made by r3ci')
        logger.info('Make sure to star the github repository')
        
        config = {}
        config['message'] = open('message.txt', 'r').read().strip()
        with open('config.json', 'r') as f:
            configcontents = json.load(f)
        config['opendms'] = configcontents['opendms']
        config['servers'] = configcontents['servers']
        
        self.setconfig('open dms', config['opendms'])
        self.setconfig('server channels', config['servers'])
        self.setstats(sentdms=0, sentchannels=0, percent=0)

        tokens = files.gettokens()
        def handler(tokens):
            threadslist = []
            lock = threadinglib.Lock()
            maxthreads = 10
            availableids = list(range(1, maxthreads + 1))

            def run(token):
                nonlocal threadslist, availableids
                with lock:
                    threadid = availableids.pop(0)
                    threadslist.append({'id': threadid, 'token': token, 'progress': 0, 'success': 0, 'status': 'Idle'})
                    self.setthreads(list(threadslist))

                discord = disccccord(token, config, stats, self)
                discord.do()

                with lock:
                    threadslist = [t for t in threadslist if t['id'] != threadid]
                    availableids.append(threadid)
                    availableids.sort()
                    self.setthreads(list(threadslist))
                    logger.info(f'Thread {threadid} finished')

            if tokens:
                for token in tokens:
                    while True:
                        with lock:
                            if len(threadslist) < maxthreads:
                                break
                        time.sleep(0.1)

                    logger.info(f'Initilizing the token {token[:30]}...')
                    t = threadinglib.Thread(target=run, args=(token,))
                    t.daemon = True
                    t.start()
            else:
                logger.error('No tokens found, add them to tokens.txt')

        threadinglib.Thread(target=handler, args=(tokens,)).start()

if __name__ == '__main__':
    app = Dashboard()
    app.run()