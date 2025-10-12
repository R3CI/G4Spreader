from src import *
from src.cli import dashboard, logger

class files:
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
