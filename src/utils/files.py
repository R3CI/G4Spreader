from src import *
from src.utils.logging import logger

class files:
    def check():
        filestomake = [
            'results'
        ]

        folderstomake = [
            'tokens.txt',
            'proxies.txt',
            'message.txt'
        ]

        for path in filestomake:
            try:
                if not os.path.exists(path):
                    os.makedirs(path)

            except PermissionError as e:
                logger.error(f'Permission denied creating files/directories, please move G4SpreadER to a different place desktop/own folder best » {e}')
                input('')

            except Exception as e:
                logger.error(f'Error creating files » {e}')
                input('')
        
        for path in folderstomake:
            try:
                if not os.path.exists(path):
                    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write('')
    
            except PermissionError as e:
                logger.error(f'Permission denied creating files/directories, please move G4SpreadER to a different place desktop/own folder best » {e}')
                input('')

            except Exception as e:
                logger.error(f'Error creating files » {e}')
                input('')

    def gettokens():
        tokens = []

        try:
            with open('tokens.txt', 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.read().splitlines()
                for line in lines:
                    if not line.strip():
                        continue

                    coloncount = line.count(':')
                    if coloncount == 1 or coloncount > 2:
                        logger.error(f'Invalid token format the correct format is EMAIL:PASSWORD:TOKEN if this IS your format keep the token only as ur supplier is a idiot » {line}')

                    parts = line.split(':', 2)
                    if len(parts) == 3:
                        email, password, token = parts
                    else:
                        token = parts[0]
                    
                    tokens.append(token)
        
        except PermissionError as e:
            logger.error(f'Permission denied reading files/directories, please move G4Spreader to a different place desktop/own folder best » {e}')
            input('')

        except Exception as e:
            logger.error(f'Error reading files » {e}')
            input('')

        return tokens
        
    def getproxies():
        proxies = []
        try:
            with open('proxies.txt', 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.read().splitlines()
                for line in lines:
                    try:
                        if '@' in line:
                            proxies.append(line)

                        else:
                            logger.error(f'Invalid proxy format the correct format is user:password@host:port » {line}')

                    except:
                        continue
                   
        except PermissionError as e:
            logger.error(f'Permission denied reading files/directories, please move G4Spreader to a different place desktop/own folder best » {e}')
            input('')
            
        except Exception as e:
            logger.error(f'Error reading files » {e}')
            input('')
               
        return proxies

    def choosefile():
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title='Select a file',
            filetypes=[
                ('All files', '*.*'),
            ]
        )
        root.destroy()
        return path

    def choosefolder():
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askdirectory(title='Select a folder')
        root.destroy()
        return path
