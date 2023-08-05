from colorama import Fore, Back, Style

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL


def printr(msg):
    print(Fore.RED + msg)


def printg(msg):
    print(Fore.GREEN + msg)


def printy(msg):
    print(Fore.YELLOW + msg)


def print_color_reset():
    print(Fore.RESET, end=" ")
