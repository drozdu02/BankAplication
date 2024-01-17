import sqlite3
import hashlib
import os
from lib.bankDB import DataBase


class ClientInterface(DataBase):
    def __init__(self, bank_database):
        super().__init__()
        self.bank_database = bank_database
        
        
    
    
    def register_client(self):
        balance = float(input("Enter your account balance: "))
        limit_withdrawal = int(input("Enter your limit withdrawal: "))
        client_id = input("Enter your client ID: ")
        login_pin = input("Enter your login PIN: ")
        help_question = input("The answer to this question will help you get your ID if forgotten. What is your mother's maiden name?")
        
        
        

        new_client_data = {
            'client_id': client_id,
            'balance': balance,
            'limit_withdrawal': limit_withdrawal,
            'login_pin': login_pin,
            'help_question' : help_question
        }

        try:
            self.cursor.execute('''
                INSERT INTO clients (client_id, balance, limit_withdrawal, login_pin, help_question)
                VALUES (?, ?, ?, ?, ?)
            ''', (client_id, balance, limit_withdrawal, login_pin, help_question))
            self.conn.commit()
            print(f"Client with ID {client_id} registered successfully.")
        except sqlite3.IntegrityError:
            print(f"Client with ID {client_id} already exists.")
            
            
                
    def client_login(self, client_id):
        login_pin = input("Enter your login PIN: ")
        self.cursor.execute('SELECT client_id FROM clients WHERE client_id=? AND login_pin=?', 
                            (client_id, login_pin))
        result = self.cursor.fetchone()
        
        if result:
            print("You logged in successfully.")
            return True
        else:
            print("Check if your client ID and PIN are correct.")
            change_pin_option = input("Do you want to reset your PIN? If so, input 'yes'.")
            
            if change_pin_option.lower() == 'yes':
                if self.lost_pin(client_id):
                    print("PIN reset successful. Please log in again.")
                else:
                    print("Unable to reset PIN. Please contact customer support.")
                    return False
            else:
                print("Invalid input. PIN reset aborted.")
                return False

        return False
                    
                
    
    def lost_pin(self, client_id):
        self.cursor.execute('SELECT help_question FROM clients WHERE client_id=?', (client_id,))
        result = self.cursor.fetchone()

        if result:
            answer = input("Enter the answer to the question: What is your mother's maiden name? ")
            if result[0] == answer:
                new_pin = input("Enter new PIN: ")
                self.cursor.execute('UPDATE clients SET login_pin=? WHERE client_id=?', (new_pin, client_id))
                self.conn.commit()
                return True
            else:
                print("Wrong answer to the security question.")
                return False
        else:
            print("Client ID not found.")
            return False    
        
    
    def delete_client(self, client_id):
        
        self.cursor.execute('''
            DELETE FROM clients WHERE client_id=?
                            ''',(client_id))
        self.conn.commit()
        print(f"Client with ID {client_id} deleted successfully.")
    
    
    def check_balance(self, client_id):
        self.cursor.execute('''
            SELECT balance FROM clients WHERE client_id=?
        ''', (client_id,))
        result = self.cursor.fetchone()
        if result:
            print(f"Your balance is: {result[0]}")
        else:
            print("Client ID not found.")
    
    def check_limit_withdrawal(self, client_id):
        self.cursor.execute('''
            SELECT limit_withdrawal FROM clients WHERE client_id=?
        ''', (client_id,))
        result = self.cursor.fetchone()
        if result:
            print(f"Your limit withdrawal is: {result[0]}")
        else:
            print("Client ID not found.")
        
    def withdraw(self, client_id):
        withdraw_amount = int(input("Enter the amount to withdraw: "))
        self.cursor.execute('''
            SELECT balance FROM clients WHERE client_id=?
        ''', (client_id,))
        current_balance = self.cursor.fetchone()
        
        if current_balance:
            if withdraw_amount <= current_balance[0]:
                new_balance = current_balance[0] - withdraw_amount
                self.cursor.execute('''
                    UPDATE clients SET balance=? WHERE client_id=?
                ''', (new_balance, client_id))
                self.conn.commit()
                print(f"Withdrawal of {withdraw_amount} successfully.")
            else:
                print("Insufficient funds or exceeds withdrawal limit.")
        else:
            print("Client ID not found.")
            
    def deposit(self, client_id):
        deposit_amount = int(input("Enter the amount to deposit: "))
        self.cursor.execute('''
            SELECT balance FROM clients WHERE client_id=?
        ''', (client_id,))
        current_balance = self.cursor.fetchone()

        if current_balance:
            new_balance = current_balance[0] + deposit_amount
            self.cursor.execute('''
                UPDATE clients SET balance=? WHERE client_id=?
            ''', (new_balance, client_id))
            self.conn.commit()
            print(f"Deposit of {deposit_amount} successfully made. Your account balance is: {new_balance}")
        else:
            print("Client ID not found.")
            
    
    def make_transfer(self, client_id):
        transfer_amount = int(input("Enter the amount to transfer: "))
        recipient_id = input("Enter the client ID you'd like to transfer to: ")
        
        if transfer_amount <= 0:
            print("Transfer amount should be a positive number.")
        self.cursor.execute('SELECT balance FROM clients WHERE client_id=?', (client_id,))
        sender_balance = self.cursor.fetchone()
        
        self.cursor.execute('SELECT balance FROM clients WHERE client_id=?', (recipient_id,))
        recipient_balance = self.cursor.fetchone()
        
        if sender_balance and recipient_balance:
            sender_balance = sender_balance[0]
            recipient_balance = recipient_balance[0]

            if transfer_amount <= sender_balance:
                new_sender_balance = sender_balance - transfer_amount
                new_recipient_balance = recipient_balance + transfer_amount
                try:
                    self.conn.execute('BEGIN TRANSACTION')
                    self.cursor.execute('UPDATE clients SET balance=? WHERE client_id=?', (new_sender_balance, client_id))
                    self.cursor.execute('UPDATE clients SET balance=? WHERE client_id=?', (new_recipient_balance, recipient_id))
                    self.conn.commit()
                    print(f"Transfer of {transfer_amount} from {client_id} to {recipient_id} successful. Your account balance is: {new_sender_balance}.")
                except sqlite3.Error:
                    self.conn.rollback()
                    print("Error occured during transfer. Try again later.")
            
            else:
                print("Insufficient funds for the transfer.")
        else:
            print("Invalid client ID.")



