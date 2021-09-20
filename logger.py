import colorama,sys
colorama.init(autoreset=True)
Fore=colorama.Fore
Back=colorama.Back
def warning(text):
    print('[{color}Warning{reset}]{message}'.format(color=Fore.YELLOW,reset=Fore.RESET,message=text))
def error(text):
    print('[{color}Error{reset}]{message}'.format(color=Fore.RED,reset=Fore.RESET,message=text))
def fatal(text):
    print('[{color}FATAL{reset}]{message}'.format(color=Fore.RED+colorama.Style.BRIGHT,reset=Fore.RESET,message=text))
    sys.exit(1)
def log(text):
    print('[{color}LOG{reset}]{message}'.format(color=Fore.BLUE,reset=Fore.RESET,message=text))