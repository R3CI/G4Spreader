from src import *
from src.utils.logging import logger

class console:
    def __init__(self, module='Console'):
        self.module = module

    def cls(self):
        os.system('cls')

    def title(self, title):
        os.system(f'title {title}')

    def center(self, text, size):
        text = str(text)
        lines = text.split('\n')
        centeredlines = []
        for line in lines:
            visibleline = re.sub(r'\033\[[0-9;]*m', '', line)
            visiblelength = len(visibleline)
            
            if visiblelength >= size:
                centeredlines.append(line)
            else:
                padding = (size - visiblelength) // 2
                centeredlines.append(' ' * padding + line)
        
        return '\n'.join(centeredlines)

    def printbar(self, tokens, proxies):
        bar = fr'{co.main}«{tokens}» Tokens                   «{proxies}» Proxies'

        bar = self.center(text=bar, size=os.get_terminal_size().columns)
        bar = str(bar)

        for char in ['»', '«']:
            bar = bar.replace(char, f'{co.main}{char}{co.reset}')

        print(bar)

    def printbanner(self):
        banner = fr'''{co.main}
   ________ __ _____                           __         
  / ____/ // // ___/____  ________  ____ _____/ /__  _____
 / / __/ // /_\__ \/ __ \/ ___/ _ \/ __ `/ __  / _ \/ ___/
/ /_/ /__  __/__/ / /_/ / /  /  __/ /_/ / /_/ /  __/ /    
\____/  /_/ /____/ .___/_/   \___/\__,_/\__,_/\___/_/     
                /_/                                       ''' 
        banner = self.center(banner, os.get_terminal_size().columns)

        print(banner)

    def input(self, text, expected=str):
        promptparts = [f'{co.main}[{co.reset}{text}{co.main}]']
        
        if expected == bool:
            promptparts.append(f'{co.main}({co.reset}{co.lime}y{co.reset}/{co.red}n{co.reset}{co.main})')
        
        prompt = ' '.join(promptparts) + f' {co.reset}» {co.reset}'
        
        while True:
            result = input(prompt).strip()
        
            if not result:
                if expected == str:
                    return result
                else:
                    logger.info('Input required please enter a value')
                    continue

            if expected == bool:
                if result.lower() in ['y', 'yes', 'true', '1']:
                    return True
                
                elif result.lower() in ['n', 'no', 'false', '0']:
                    return False
                
                else:
                    logger.info('Invalid input please enter y/yes/true or n/no/false')
                    continue
            
            if expected == str:
                return result
            
            try:
                converted = expected(result)
                return converted
                
            except ValueError:
                if expected == int:
                    logger.info('Please enter a whole number (eg 1 42 100)')

                elif expected == float:
                    logger.info('Please enter a decimal number (eg 1.5 3.14 10.0)')

                else:
                    logger.info(f'Invalid format expected {expected.__name__}')
                continue

    def prep(self):
        self.cls()
        self.printbanner()
        if self.module != None:
            self.title(f'G4Spreader - {self.module} - g4tools.cc - discord.gg/spamming - Made by r3ci')