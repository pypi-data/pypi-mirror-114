import os, sys, platform

WIN = False
LINUX = False

if platform.system() == "Windows":
    WIN = True
    os.system("")
else:
    LINUX = True

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


def getfgfromrgb(r, g, b):
    return "\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"

def getbgfromrgb(r, g, b):
    return "\033[48;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"

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

def setColor(color):
    cprint(color, end="")

def reset():
    cprint(style.RESET, end="")

if WIN:
    class cmd:
        def setname(name):
            cprint("\x1b]0;" + name + "\x07", end="")

        def clear():
            os.system("cls")

        def showcursor():
            cprint("\x1b[?25h", end="")

        def hidecursor():
            cprint("\x1b[?25l", end="")

        def startcursorblinking():
            cprint("\x1b[?12h", end="")

        def stopcursorblinking():
            cprint("\x1b[?12l", end="")

        def createscreenbuffer():
            cprint("\x1b[?1049h", end="")

        def switchtomainscreenbuffer():
            cprint("\x1b[?1049l", end="")

        def movecursor(x, y):
            cprint("\x1b[" + str(x) + ";" + str(y) + "H", end="")

        def printtoline(line, msg):
            cmd.movecursor(line, 0)
            cprint(msg, end="\r")
