from typing import Literal

from colorama import Fore, Style


FORES = {
    'COMPLETE': Fore.BLUE,
    'ERROR': Fore.RED,
    'INFO': Fore.WHITE,
    'INITIATE': Fore.CYAN,
    'SUCCESS': Fore.GREEN,
}

STYLES = {
    'COMPLETE': Style.BRIGHT,
    'SUCCESS': Style.BRIGHT
}


def log_message(type: Literal['SUCCESS', 'INFO', 'ERROR', 'COMPLETE'] = '', msg: str = ''):
    fore = FORES.get(type, '')
    style = STYLES.get(type, '')
            
    print(f'{style}{fore}{msg}')
