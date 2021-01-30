from random import randint
import sys
from DB_Connection import db_update


class User:
    account = {}

    def __init__(self, name, deposit):
        if deposit < 500:
            print("Sorry, Minimum Deposit Amount is 500 USD !!")
            self.account['holdings'] = None
            self.account['account_number'] = None
            self.account['name'] = None
        else:
            self.account['holdings'] = deposit
            self.account['account_number'] = randint(10000, 99999)
            self.account['name'] = name

    def withdraw(self, amount, account_number):
        if self.account['holdings'] >= amount:
            self.account['holdings'] -= amount
            db_update(account_number, self.account['holdings'])
            print("Amount withdrawn from your account {}.".format(amount))
            self.balance()

        else:
            print("Not enough Funds!!")
            self.balance()

    def deposit(self, amount, account_number):
        self.account['holdings'] += amount
        db_update(account_number, self.account['holdings'])
        print("The sum of {} has been added to your account balance.".format(amount))
        self.balance()

    def balance(self):
        print()
        print("Your current account balance is {}".format(self.account['holdings']))
