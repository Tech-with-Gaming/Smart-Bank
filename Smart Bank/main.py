import colorama
from colorama import Fore, Style
import os
import time
import sys

colorama.init()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(Fore.WHITE + Style.BRIGHT + r"""________                        _____  ________              ______  
__  ___/______ _________ _________  /_ ___  __ )_____ __________  /__
_____ \__  __ `__ \  __ `/_  ___/  __/ __  __  |  __ `/_  __ \_  //_/
____/ /_  / / / / / /_/ /_  /   / /_   _  /_/ // /_/ /_  / / /  ,<   
/____/ /_/ /_/ /_/\__,_/ /_/    \__/   /_____/ \__,_/ /_/ /_//_/|_|   """ + Style.RESET_ALL)


def typing_animation(text, delay=0.05):
    for char in text:
        sys.stdout.write(Fore.WHITE + Style.BRIGHT + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    time.sleep(0.5)
 
 
def loading_animation():
    print(Fore.WHITE + Style.BRIGHT + "Loading", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(" ✓" + Style.RESET_ALL)
    time.sleep(1)


def main():
    print_banner()
    typing_animation("Welcome to Smart Bank! Starting up the system, Please Wait...")
    loading_animation()
    
    from interface import main_menu
    main_menu()


if __name__ == "__main__":
    main()
