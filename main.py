import sys, os; sys.dont_write_bytecode = True; os.environ['PYTHONDONTWRITEBYTECODE'] = '1'; os.system('cls'); os.system('title G4Spreader - launching...')
from src import *
from src.utils.logging import logger
from src.utils.files import files
from src.utils.console import console; console=console('Main')

while True:
    console.cls()
    console.title('G4Spreader - g4tools.cc - discord.gg/spamming - Made by r3ci')
    console.printbanner()
    console.printbar(len(files.gettokens()), len(files.getproxies()))
    logger.info('Make sure to star the github repository', 'Main')
    if open('message.txt', 'r').read().strip() == '':
        with open('message.txt', 'w', encoding='utf-8', errors='ignore') as f:
            f.write(console.input('Message (will be saved to message.txt and then reused)', str).strip())
    
    config = {}
    config['message'] = open('message.txt', 'r').read().strip()
    config['opendms'] = console.input('Send to open DMS', bool)
    config['servers'] = console.input('Send to servers', bool)