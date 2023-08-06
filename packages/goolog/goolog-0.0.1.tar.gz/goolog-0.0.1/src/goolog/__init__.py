from datetime import datetime


class ConsoleColors(object):
    SUCCESS_COLOR = '\033[32m'
    WARNING_COLOR = '\033[93m'
    ERROR_COLOR = '\033[31m'
    FATAL_COLOR = '\033[91m'
    END_COLOR = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def info(msg):
    print(f'>> {get_time()}: {msg}')


def suc(msg):
    print(f'>> {get_time()}: {ConsoleColors.SUCCESS_COLOR}{msg}{ConsoleColors.END_COLOR}')


def warn(msg):
    print(f'>> {get_time()}: {ConsoleColors.WARNING_COLOR}{msg}{ConsoleColors.END_COLOR}')


def err(msg):
    print(f'>> {get_time()}: {ConsoleColors.ERROR_COLOR}{msg}{ConsoleColors.END_COLOR}')


def fatal(msg):
    print(f'>> {get_time()}: {ConsoleColors.FATAL_COLOR}{msg}{ConsoleColors.END_COLOR}')
