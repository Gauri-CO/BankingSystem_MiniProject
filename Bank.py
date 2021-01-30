from DB_Connection import db_insert, db_select
from User import User


class Bank:
    name = "United States Bank"
    users = []

    def update_db(self, user):
        self.users.append(user)
        db_insert(user)

    def authentication(self, name, account_number):
        results = db_select(name, account_number)

        for val in results:
            if val.name and val.account_number:
                check_user = User(val.name, val.holdings)
                print()
                print("Authentication successful!")
                return check_user
