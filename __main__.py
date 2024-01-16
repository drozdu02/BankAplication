import sqlite3
import hashlib
import os
from lib.bankDB import DataBase
from lib.clientRepository import ClientInterface
    
                            

if __name__ == '__main__':
    

    bank_dB = DataBase()
    client = ClientInterface(bank_dB)
    
    while True:
        print("\nWelcome to the Drozdowski's Bank!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            client.register_client()
        elif choice == '2':
            client_id = input("Enter your client ID :")
            client.client_login(client_id)
            while True:
                print("\nLogged in as", client_id)
                print("1. Check Balance")
                print("2. Check limit withdrawal")
                print("3. Deposit")
                print("4. Withdraw")
                print("5. Delete account")
                print("6. Logout")
                option = input("Choose an option (1/2/3/4/5): ")
                if option == '1':
                    client.check_balance(client_id)
                elif option == '2':
                    client.check_limit_withdrawal(client_id)
                elif option == '3':
                    client.deposit(client_id)
                elif option == '4':
                    client.withdraw(client_id)
                elif option == '5':
                    client.delete_client(client_id)
                elif option == '6':
                    print("Logging out...")
                    break
                else:
                    print("Invalid option. Please try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")