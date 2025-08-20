import colorama
from colorama import Fore, Style
import os
import time
from account import BankAccount, check_pin_exists
from main import clear_screen
import pwinput




def main_menu():
    while True:
        clear_screen()
        print(Fore.YELLOW + r""" __  __       _         __  __                  
|  \/  | __ _(_)_ __   |  \/  | ___ _ __  _   _ 
| |\/| |/ _` | | '_ \  | |\/| |/ _ \ '_ \| | | |
| |  | | (_| | | | | | | |  | |  __/ | | | |_| |
|_|  |_|\__,_|_|_| |_| |_|  |_|\___|_| |_|\__,_|""" + Style.BRIGHT + Style.RESET_ALL)
        
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.GREEN + "[1] [+] Create New Account")
        print(Fore.GREEN + "[2] [>] User Login") 
        print(Fore.GREEN + "[3] [#] Admin Panel")
        print(Fore.GREEN + "[4] [<<] Exit")
        print(Fore.CYAN + "="*50 + Style.RESET_ALL)
        
        choice = input(Fore.GREEN + "Enter your Choice [1-4]: " + Style.BRIGHT + Style.RESET_ALL)
        
        if choice == "1":
            clear_screen()
            print(Fore.BLUE + "1. Create Account:- " + Style.BRIGHT + Style.RESET_ALL)
            create_account_interface()
        elif choice == "2":
            clear_screen()
            print(Fore.BLUE + "2. User Login:- " + Style.BRIGHT + Style.RESET_ALL)
            user_login()
        elif choice == "3":
            clear_screen()
            admin_pin()
        elif choice == "4":
            clear_screen()
            exit_banner()
            break
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid Choice" + Style.RESET_ALL)
        
        input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)



def admin_pin():
    from admin import admin_login, admin_menu
    
    if admin_login():
        admin_menu()
    else:
        print(Fore.RED + "Access Denied. Returning to main menu..." + Style.RESET_ALL)



def admin_banner():
    print(Fore.RED + r"""   _      _       _        ___               _ 
  /_\  __| |_ __ (_)_ _   | _ \__ _ _ _  ___| |
 / _ \/ _` | '  \| | ' \  |  _/ _` | ' \/ -_) |
/_/ \_\__,_|_|_|_|_|_||_| |_| \__,_|_||_\___|_| """ + Style.BRIGHT + Style.RESET_ALL)



def exit_banner():
    print(Fore.CYAN + r""" _____ _              _    __   __        _ 
|_   _| |_  __ _ _ _ | |__ \ \ / /__ _  _| |
  | | | ' \/ _` | ' \| / /  \ V / _ \ || |_|
  |_| |_||_\__,_|_||_|_\_\   |_|\___/\_,_(_) """ + Style.BRIGHT + Style.RESET_ALL)



def user_login():
    print(Fore.YELLOW + Style.BRIGHT + "=== USER LOGIN ===" + Style.RESET_ALL)
    
    while True:
        acc_input = input(Fore.CYAN + "Enter your Account Number: " + Style.RESET_ALL)
        if acc_input.isdigit():
            account_number = int(acc_input)
            break
        print(Fore.RED + "[X] Please enter a valid account number!" + Style.RESET_ALL)
    
    while True:
        pin = pwinput.pwinput(prompt=Fore.CYAN + "Enter your 4-digit PIN: " + Style.RESET_ALL, mask="*")
        if len(pin) == 4 and pin.isdigit():
            break
        print(Fore.RED + "[X] PIN must be exactly 4 digits!" + Style.RESET_ALL)
    

    from account import load_account_from_database
    account = load_account_from_database(account_number, pin)
    

    if account:
        print(Fore.GREEN + Style.BRIGHT + "\n[+] Login Successful!" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Welcome back, {account.first_name} {account.last_name}!" + Style.RESET_ALL)
        
        account_menu(account)
    else:
        print(Fore.RED + Style.BRIGHT + "\n[X] Invalid Account Number or PIN!" + Style.RESET_ALL)
        print(Fore.CYAN + "Please check your credentials and try again." + Style.RESET_ALL)



def account_menu(account):
    while True:
        clear_screen()
        print(Fore.YELLOW + Style.BRIGHT + f"=== ACCOUNT MENU - {account.first_name} {account.last_name} ===" + Style.RESET_ALL)
        print(Fore.CYAN + f"Account Number: {account.account_number}" + Style.RESET_ALL)
        
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.GREEN + "[1] [$] View Balance")
        print(Fore.GREEN + "[2] [>>] Deposit Money") 
        print(Fore.GREEN + "[3] [<<] Withdraw Money")
        print(Fore.GREEN + "[4] [>] Change PIN")
        print(Fore.GREEN + "[5] [*] Change Name")
        print(Fore.GREEN + "[6] [<<] Logout")
        print(Fore.CYAN + "="*50 + Style.RESET_ALL)
        
        choice = input(Fore.GREEN + "Enter your Choice [1-6]: " + Style.RESET_ALL)
        
        if choice == "1":
            display_balance(account)
        elif choice == "2":
            deposit_money(account)
        elif choice == "3":
            withdraw_money(account)
        elif choice == "4":
            change_pin_interface(account)
        elif choice == "5":
            change_name_interface(account)
        elif choice == "6":
            print(Fore.CYAN + "[<<] Logging out... Thank you for using Smart Bank!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "[X] Invalid choice! Please try again." + Style.RESET_ALL)
        
        input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)



def display_balance(account):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== ACCOUNT BALANCE ===" + Style.RESET_ALL)
    balance = account.view_balance()
    print(Fore.GREEN + f"[$] Current Balance: ${balance:,.2f}" + Style.RESET_ALL)



def deposit_money(account):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== DEPOSIT MONEY ===" + Style.RESET_ALL)
    while True:
        amount_input = input(Fore.CYAN + "Enter amount to deposit ($): " + Style.RESET_ALL)
        try:
            amount = float(amount_input)
            if amount > 0:
                if account.deposit(amount):
                    print(Fore.GREEN + f"[+] Successfully deposited ${amount:,.2f}" + Style.RESET_ALL)
                    print(Fore.YELLOW + f"[$] New Balance: ${account.view_balance():,.2f}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "[X] Deposit failed!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "[X] Amount must be positive!" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[X] Please enter a valid number!" + Style.RESET_ALL)



def withdraw_money(account):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== WITHDRAW MONEY ===" + Style.RESET_ALL)
    print(Fore.CYAN + f"Available Balance: ${account.view_balance():,.2f}" + Style.RESET_ALL)
    
    while True:
        amount_input = input(Fore.CYAN + "Enter amount to withdraw ($): " + Style.RESET_ALL)
        try:
            amount = float(amount_input)
            if amount > 0:
                if account.withdraw(amount):
                    print(Fore.GREEN + f"[+] Successfully withdrew ${amount:,.2f}" + Style.RESET_ALL)
                    print(Fore.YELLOW + f"[$] New Balance: ${account.view_balance():,.2f}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "[X] Insufficient funds or invalid amount!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "[X] Amount must be positive!" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[X] Please enter a valid number!" + Style.RESET_ALL)



def change_pin_interface(account):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== CHANGE PIN ===" + Style.RESET_ALL)
    
    while True:
        new_pin = input(Fore.CYAN + "Enter new 4-digit PIN: " + Style.RESET_ALL)
        if len(new_pin) == 4 and new_pin.isdigit():
            if account.change_pin(new_pin):
                print(Fore.GREEN + "[+] PIN changed successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "[X] Failed to change PIN!" + Style.RESET_ALL)
            break
        print(Fore.RED + "[X] PIN must be exactly 4 digits!" + Style.RESET_ALL)



def change_name_interface(account):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== CHANGE NAME ===" + Style.RESET_ALL)
    print(Fore.CYAN + f"Current Name: {account.first_name} {account.last_name}" + Style.RESET_ALL)
    
    while True:
        new_first = input(Fore.CYAN + "Enter new First Name: " + Style.RESET_ALL).strip()
        if len(new_first) >= 2 and new_first.isalpha():
            break
        print(Fore.RED + "[X] First name must be at least 2 letters!" + Style.RESET_ALL)
    
    while True:
        new_last = input(Fore.CYAN + "Enter new Last Name: " + Style.RESET_ALL).strip()
        if len(new_last) >= 2 and new_last.isalpha():
            break
        print(Fore.RED + "[X] Last name must be at least 2 letters!" + Style.RESET_ALL)
    
    if account.change_name(new_first, new_last):
        print(Fore.GREEN + f"[+] Name changed successfully to: {new_first} {new_last}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[X] Failed to change name!" + Style.RESET_ALL)



def create_account_interface():
    print(Fore.YELLOW + Style.BRIGHT + "=== CREATE NEW ACCOUNT ===" + Style.RESET_ALL)
    
    while True:
        first_name = input(Fore.CYAN + "Enter your First Name: " + Style.RESET_ALL).strip()
        if len(first_name) >= 2 and first_name.isalpha():
            break
        print(Fore.RED + "[X] First name must be at least 2 letters and contain only alphabets!" + Style.RESET_ALL)
    
    while True:
        last_name = input(Fore.CYAN + "Enter your Last Name: " + Style.RESET_ALL).strip()
        if len(last_name) >= 2 and last_name.isalpha():
            break
        print(Fore.RED + "[X] Last name must be at least 2 letters and contain only alphabets!" + Style.RESET_ALL)
    
    while True:
        pin = pwinput.pwinput(prompt=Fore.CYAN + "Enter your 4-digit PIN: " + Style.RESET_ALL, mask="*")
        if len(pin) == 4 and pin.isdigit():
            if not check_pin_exists(pin):
                break
            else:
                print(Fore.RED + "[X] This PIN is already in use. Please choose a different one." + Style.RESET_ALL)
        print(Fore.RED + "[X] PIN must be exactly 4 digits!" + Style.RESET_ALL)
    
    while True:
        balance_input = input(Fore.CYAN + "Enter Your Initial Deposit Amount ($): " + Style.RESET_ALL)
        try:
            balance = float(balance_input)
            if balance >= 0:
                break
            else:
                print(Fore.RED + "[X] Amount cannot be negative!" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[X] Please enter a valid number!" + Style.RESET_ALL)

    try:
        account_created = BankAccount(first_name, last_name, pin, balance)
        account_number = account_created.save_to_database()
        
        print(Fore.GREEN + Style.BRIGHT + "\n[+] Account Created Successfully!" + Style.RESET_ALL)
        print(Fore.YELLOW + f"[>] Your Account Number: {account_number}")
        print(Fore.YELLOW + f"[>] Account Holder: {first_name} {last_name}")
        print(Fore.YELLOW + f"[$] Initial Balance: ${balance:,.2f}" + Style.RESET_ALL)
        print(Fore.CYAN + "\n[!] Please remember your account number and PIN for login!" + Style.RESET_ALL)
        
    except Exception as e:
        print(Fore.RED + f"[X] Error creating account: {str(e)}" + Style.RESET_ALL)
