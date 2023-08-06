import os, sys, platform

if platform.system() == "Windows":
	os.system("")

class style:
    """
    Foreground normal
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    """
    Foreground bright
    """
    BLACK_BRIGHT = '\033[30;1m'
    RED_BRIGHT = '\033[31;1m'
    GREEN_BRIGHT = '\033[32;1m'
    YELLOW_BRIGHT = '\033[33;1m'
    BLUE_BRIGHT = '\033[34;1m'
    MAGENTA_BRIGHT = '\033[35;1m'
    CYAN_BRIGHT = '\033[36;1m'
    WHITE_BRIGHT = '\033[37;1m'

    """
    Background normal
    """
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    """
    Background bright
    """
    BG_BLACK_BRIGHT = '\033[40;1m'
    BG_RED_BRIGHT = '\033[41;1m'
    BG_GREEN_BRIGHT = '\033[42;1m'
    BG_YELLOW_BRIGHT = '\033[43;1m'
    BG_BLUE_BRIGHT = '\033[44;1m'
    BG_MAGENTA_BRIGHT = '\033[45;1m'
    BG_CYAN_BRIGHT = '\033[46;1m'
    BG_WHITE_BRIGHT = '\033[47;1m'

    """
    Font style
    """
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'

    """
    Reset the output
    """
    RESET = '\033[0m'


class style_handler:
    def __init__(self):
        self.styles_dict = self._getAllStyles()

    def _getAllStyles(self):
        return vars(style)

    def getAllStyles(self):
        styles_list = list(self.styles_dict.keys())
        del styles_list[:2]
        del styles_list[len(styles_list) - 2:]

        return styles_list

    def getStyleByKey(self, key):
        return self.styles_dict.get(key)


def cprint(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
    sep = style.RESET + sep

    if len(args) > 1:
        for msg in args:
            msg = str(msg)
            if msg == args[len(args) - 1]:
                print(msg + style.RESET, end=end, file=file, flush=flush)
            else:
                print(msg, end="", file=file, flush=flush)
                print(sep, end="")
    else:
        for msg in args:
            msg = str(msg)
            print(msg + style.RESET, end=end, file=file, flush=flush)

def cinput(prompt):
    return input(prompt + style.RESET)

def reset():
    print(style.RESET)
