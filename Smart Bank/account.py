import sqlite3


class BankAccount:
    def __init__(self, first_name, last_name, pin, balance=0):
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.balance = balance
        self.account_number = None



    def create_accounts(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts (
                       Acc_Number INTEGER PRIMARY KEY,
                       First_Name TEXT NOT NULL CHECK(length(First_Name) >= 2),
                       Last_Name TEXT NOT NULL CHECK(length(Last_Name) >= 2),
                       Pin TEXT NOT NULL UNIQUE CHECK(length(Pin) = 4 AND Pin GLOB '[0-9][0-9][0-9][0-9]'),
                       Balance REAL DEFAULT 0 CHECK(Balance >= 0),
                       Creation_Date TEXT DEFAULT CURRENT_TIMESTAMP
                       )""")
        
        conn.commit()
        conn.close()



    def save_to_database(self):
        self.create_accounts()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""INSERT INTO Accounts (First_Name, Last_Name, Pin, Balance) 
                             VALUES (?, ?, ?, ?)""", 
                          (self.first_name, self.last_name, self.pin, self.balance))
            
            self.account_number = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.account_number
            
        except sqlite3.IntegrityError as e:
            conn.close()
            if "UNIQUE constraint failed: Accounts.Pin" in str(e):
                raise ValueError("PIN_ALREADY_EXISTS")
            else:
                raise ValueError("DATABASE_ERROR")



    def view_balance(self):
        return self.balance



    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.update_balance_in_database()
            return True
        return False



    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.update_balance_in_database()
            return True
        return False



    def change_pin(self, new_pin):
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            self.update_pin_in_database()
            return True
        return False



    def change_name(self, new_first_name, new_last_name):
        if len(new_first_name) >= 2 and len(new_last_name) >= 2:
            self.first_name = new_first_name
            self.last_name = new_last_name
            self.update_name_in_database()
            return True
        return False



    def update_balance_in_database(self):
        if self.account_number:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE Accounts SET Balance = ? WHERE Acc_Number = ?", 
                          (self.balance, self.account_number))
            conn.commit()
            conn.close()



    def update_pin_in_database(self):
        if self.account_number:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE Accounts SET Pin = ? WHERE Acc_Number = ?", 
                          (self.pin, self.account_number))
            conn.commit()
            conn.close()



    def update_name_in_database(self):
        if self.account_number:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE Accounts SET First_Name = ?, Last_Name = ? WHERE Acc_Number = ?", 
                          (self.first_name, self.last_name, self.account_number))
            conn.commit()
            conn.close()



    def get_account_info(self):
        return {
            'account_number': self.account_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'balance': self.balance
        }



def check_pin_exists(pin):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts (
                       Acc_Number INTEGER PRIMARY KEY,
                       First_Name TEXT NOT NULL CHECK(length(First_Name) >= 2),
                       Last_Name TEXT NOT NULL CHECK(length(Last_Name) >= 2),
                       Pin TEXT NOT NULL UNIQUE CHECK(length(Pin) = 4 AND Pin GLOB '[0-9][0-9][0-9][0-9]'),
                       Balance REAL DEFAULT 0 CHECK(Balance >= 0),
                       Creation_Date TEXT DEFAULT CURRENT_TIMESTAMP
                       )""")
        
        cursor.execute("SELECT COUNT(*) FROM Accounts WHERE Pin = ?", (pin,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] > 0
        
    except sqlite3.OperationalError:
        return False



def load_account_from_database(account_number, pin):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Accounts WHERE Acc_Number = ? AND Pin = ?", 
                    (account_number, pin))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            account = BankAccount(result[1], result[2], result[3], result[4])
            account.account_number = result[0]
            return account
        return None
    except sqlite3.OperationalError:
        print("❌ Database error occurred while loading account.")



def get_all_accounts():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Accounts")
    results = cursor.fetchall()
    conn.close()
    
    return results



def delete_account_from_database(account_number):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Accounts WHERE Acc_Number = ?", (account_number,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
