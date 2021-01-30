from User import User
from Bank import Bank

if __name__ == '__main__':
    bank = Bank()
    print()
    print("Welcome to {}!".format(bank.name))
    print()
    running = True

    while running:

        print()
        print(""" Chose an option:
        
        1. Open a new bank account
        2. Open existing bank account
        3. Exit
        """)

        choice = int(input("Input 1, 2 or 3:"))

        if choice == 1:
            print()
            print("To create an account , please fill in the information below:")
            print()
            user = User(input("Name:"), int(input("Deposit amount:")))
            if user.account['name'] is None:
                print("Please re-enter correct amount")
                running = False
            else:
                bank.update_db(user)
                print()
                print("Account created successfully , your account no is: ", user.account['account_number'])
        elif choice == 2:
            print()
            print("To access your account , please enter the credentials below.")
            print()
            name = input("Name:")
            account_number = int(input("Account Number :  "))
            current_user = bank.authentication(name, account_number)
            if current_user:
                print()
                print("Welcome {}!".format(current_user.account['name']))
                acc_open = True
                while acc_open:
                    print()
                    print("""Choose an option:
                    
                1. Withdraw
                2. Deposit
                3. Balance
                4. Exit
                    
                    """)
                    acc_choice = int(input("Input 1, 2, 3 or 4 : "))
                    if acc_choice == 1:
                        print()
                        current_user.withdraw(int(input("Amount to Withdraw: ")), account_number)

                    elif acc_choice == 2:
                        print()
                        current_user.deposit(int(input("Amount to Deposit: ")), account_number)
                    elif acc_choice == 3:
                        print()
                        current_user.balance()
                    elif acc_choice == 4:
                        print()
                        print("Thank you for visiting the bank")
                        current_user = ''
                        acc_open = False
            else:
                print()
                print("Authentication Failed!")
                print("Reason: account not found.")
                continue
        elif choice == 3:
            print()
            print("GoodBye!!")
            running = False
