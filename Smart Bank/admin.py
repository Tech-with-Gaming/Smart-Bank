import colorama
from colorama import Fore, Style
import sqlite3
import os
import pwinput
from account import get_all_accounts, delete_account_from_database, load_account_from_database, BankAccount

colorama.init()
ADMIN_PIN = "2008"




def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")



def admin_login():
    print(Fore.RED + Style.BRIGHT + "=== ADMIN LOGIN ===" + Style.RESET_ALL)
    
    while True:
        admin_pin = pwinput.pwinput(prompt=Fore.CYAN + "Enter Admin PIN: " + Style.RESET_ALL, mask="*")
        if admin_pin == ADMIN_PIN:
            print(Fore.GREEN + "[+] Access Granted!" + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + "[X] Invalid PIN! Access Denied." + Style.RESET_ALL)
            retry = input(Fore.YELLOW + "Try again? (y/n): " + Style.RESET_ALL).lower()
            if retry != 'y':
                return False



def remove_account():
    print(Fore.RED + Style.BRIGHT + "\n=== REMOVE ACCOUNT ===" + Style.RESET_ALL)
    
    accounts = get_all_accounts()
    if not accounts:
        print(Fore.YELLOW + "No accounts found in the database." + Style.RESET_ALL)
        return
    
    print(Fore.CYAN + "\nCurrent Accounts:")
    print("-" * 80)
    print(f"{'Acc No':<8} {'Name':<25} {'PIN':<6} {'Balance':<12} {'Created':<20}")
    print("-" * 80)
    
    for account in accounts:
        acc_num, first_name, last_name, pin, balance, created = account
        full_name = f"{first_name} {last_name}"
        print(f"{acc_num:<8} {full_name:<25} {pin:<6} ${balance:<11.2f} {created:<20}")
    
    print("-" * 80 + Style.RESET_ALL)
    
    while True:
        try:
            acc_input = input(Fore.CYAN + "\nEnter Account Number to delete (0 to cancel): " + Style.RESET_ALL)
            if acc_input == "0":
                print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL)
                return
            
            account_number = int(acc_input)
            
            account_exists = any(acc[0] == account_number for acc in accounts)
            if not account_exists:
                print(Fore.RED + "[X] Account number not found!" + Style.RESET_ALL)
                return
            
            account_data = next(acc for acc in accounts if acc[0] == account_number)
            full_name = f"{account_data[1]} {account_data[2]}"
            
            print(Fore.YELLOW + f"[!] You are about to delete account:")
            print(f"   Account Number: {account_number}")
            print(f"   Account Holder: {full_name}")
            print(f"   Balance: ${account_data[4]:,.2f}" + Style.RESET_ALL)
            
            confirm = input(Fore.RED + "Are you sure? Type 'DELETE' to confirm: " + Style.RESET_ALL)
            
            if confirm == "DELETE":
                if delete_account_from_database(account_number):
                    print(Fore.GREEN + f"[+] Account {account_number} deleted successfully!" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "[X] Failed to delete account!" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
            break
            
        except ValueError:
            print(Fore.RED + "[X] Please enter a valid account number!" + Style.RESET_ALL)



def admin_change_pin():
    print(Fore.YELLOW + Style.BRIGHT + "\n=== ADMIN CHANGE USER PIN ===" + Style.RESET_ALL)
    
    while True:
        try:
            acc_input = input(Fore.CYAN + "Enter Account Number (0 to cancel): " + Style.RESET_ALL)
            if acc_input == "0":
                print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL)
                return
            
            account_number = int(acc_input)
            break
        except ValueError:
            print(Fore.RED + "[X] Please enter a valid account number!" + Style.RESET_ALL)
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Accounts WHERE Acc_Number = ?", (account_number,))
    result = cursor.fetchone()
    
    if not result:
        print(Fore.RED + "[X] Account not found!" + Style.RESET_ALL)
        conn.close()
        return
    
    print(Fore.CYAN + f"\nAccount Found:")
    print(f"Account Number: {result[0]}")
    print(f"Account Holder: {result[1]} {result[2]}")
    print(f"Current PIN: {result[3]}")
    print(f"Balance: ${result[4]:,.2f}" + Style.RESET_ALL)
    
    while True:
        new_pin = input(Fore.CYAN + "Enter new 4-digit PIN: " + Style.RESET_ALL)
        if len(new_pin) == 4 and new_pin.isdigit():
            cursor.execute("SELECT COUNT(*) FROM Accounts WHERE Pin = ? AND Acc_Number != ?", (new_pin, account_number))
            if cursor.fetchone()[0] > 0:
                print(Fore.RED + "[X] This PIN is already in use by another account!" + Style.RESET_ALL)
                continue
            
            cursor.execute("UPDATE Accounts SET Pin = ? WHERE Acc_Number = ?", (new_pin, account_number))
            conn.commit()
            print(Fore.GREEN + f"[+] PIN changed successfully for account {account_number}!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "[X] PIN must be exactly 4 digits!" + Style.RESET_ALL)
    
    conn.close()



def clear_database():
    print(Fore.RED + Style.BRIGHT + "\n=== CLEAR DATABASE ===" + Style.RESET_ALL)
    
    accounts = get_all_accounts()
    account_count = len(accounts)
    
    if account_count == 0:
        print(Fore.YELLOW + "Database is already empty." + Style.RESET_ALL)
        return
    
    print(Fore.YELLOW + f"[!] WARNING: This will delete ALL {account_count} accounts!")
    print("This action cannot be undone!" + Style.RESET_ALL)
    
    confirm1 = input(Fore.RED + "Type 'CLEAR' to proceed: " + Style.RESET_ALL)
    if confirm1 != "CLEAR":
        print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL)
        return
    
    confirm2 = input(Fore.RED + "Are you absolutely sure? Type 'YES': " + Style.RESET_ALL)
    if confirm2 != "YES":
        print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL)
        return
    
    confirm3 = input(Fore.RED + "Final confirmation - Type 'DELETE ALL': " + Style.RESET_ALL)
    if confirm3 != "DELETE ALL":
        print(Fore.YELLOW + "Operation cancelled." + Style.RESET_ALL)
        return
    
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Accounts")
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        
        print(Fore.GREEN + f"[+] Database cleared! {deleted_count} accounts deleted." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[X] Error clearing database: {str(e)}" + Style.RESET_ALL)



def view_all_accounts():
    print(Fore.CYAN + Style.BRIGHT + "\n=== ALL ACCOUNTS ===" + Style.RESET_ALL)
    
    accounts = get_all_accounts()
    
    if not accounts:
        print(Fore.YELLOW + "No accounts found in the database." + Style.RESET_ALL)
        return
    
    print(Fore.GREEN + f"\nTotal Accounts: {len(accounts)}")
    print(Fore.CYAN + "=" * 90)
    print(f"{'Acc No':<8} {'First Name':<15} {'Last Name':<15} {'PIN':<6} {'Balance':<12} {'Created':<20}")
    print("=" * 90)
    
    total_balance = 0
    for account in accounts:
        acc_num, first_name, last_name, pin, balance, created = account
        total_balance += balance
        print(f"{acc_num:<8} {first_name:<15} {last_name:<15} {pin:<6} ${balance:<11.2f} {created:<20}")
    
    print("=" * 90)
    print(Fore.YELLOW + f"Total Bank Balance: ${total_balance:,.2f}" + Style.RESET_ALL)



def admin_menu():
    while True:
        clear_screen()
        print(Fore.RED + Style.BRIGHT + r"""   _      _       _        ___               _ 
  /_\  __| |_ __ (_)_ _   | _ \__ _ _ _  ___| |
 / _ \/ _` | '  \| | ' \  |  _/ _` | ' \/ -_) |
/_/ \_\__,_|_|_|_|_|_||_| |_| \__,_|_||_\___|_|""" + Style.RESET_ALL)
        
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.GREEN + "[1] [>] View All Accounts")
        print(Fore.GREEN + "[2] [X] Remove Account")
        print(Fore.GREEN + "[3] [>] Change User PIN")
        print(Fore.GREEN + "[4] [X] Clear Database")
        print(Fore.GREEN + "[5] [<<] Back to Main Menu")
        print(Fore.CYAN + "="*50 + Style.RESET_ALL)
        
        choice = input(Fore.GREEN + "Enter your Choice [1-5]: " + Style.RESET_ALL)
        
        if choice == "1":
            view_all_accounts()
        elif choice == "2":
            remove_account()
        elif choice == "3":
            admin_change_pin()
        elif choice == "4":
            clear_database()
        elif choice == "5":
            print(Fore.CYAN + "Returning to main menu..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "[X] Invalid choice! Please try again." + Style.RESET_ALL)
        
        input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)
