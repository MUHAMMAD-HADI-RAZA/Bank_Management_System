from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(self, balance=0):
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: +{amount}")

    @abstractmethod
    def withdraw(self, amount):
        pass

    def balance_enquiry(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions


class CheckingAccount(Account):
    def __init__(self, balance=0, credit_limit=0, overdraft_fee=0):
        super().__init__(balance)
        self.credit_limit = credit_limit
        self.overdraft_fee = overdraft_fee

    def withdraw(self, amount):
        if self.balance + self.credit_limit >= amount:
            self.balance -= amount
            if self.balance < 0:
                self.balance -= self.overdraft_fee
            self.transactions.append(f"Withdrawal: -{amount} (Overdraft Fee: -{self.overdraft_fee})")
            return True
        return False


class SavingAccount(Account):
    def __init__(self, balance=0, interest_rate=0):
        super().__init__(balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -{amount}")
            return True
        return False

    def credit_interest(self):
        interest = self.balance * self.interest_rate / 100
        self.balance += interest
        self.transactions.append(f"Interest Credited: +{interest}")


class LoanAccount(Account):
    def __init__(self, balance=0, principal_amount=0, interest_rate=0, loan_duration=0):
        super().__init__(balance)
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.loan_duration = loan_duration

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -{amount}")
            return True
        return False

    def debit_interest(self):
        interest = self.balance * self.interest_rate / 100
        self.balance += interest
        self.transactions.append(f"Interest Charged: +{interest}")



class Customer:
    def __init__(self, username, password, first_name, last_name, address):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.accounts = []

    def create_account(self, account):
        self.accounts.append(account)

    def get_account_balance(self, account_type):
        for account in self.accounts:
            if isinstance(account, account_type):
                return account.balance_enquiry()
        return None

    def deposit(self, account_type, amount):
        for account in self.accounts:
            if isinstance(account, account_type):
                account.deposit(amount)
                return True
        return False
    def withdraw(self, account_type, amount):
        for account in self.accounts:
            if isinstance(account, account_type):
                success = account.withdraw(amount)
                if success:
                    self.save_transaction_history()  # Save transaction history after a successful withdrawal
                    return True
        return False
    def print_account_balances(self):
        for account in self.accounts:
            print(f"Account Type: {type(account).__name__}, Balance: {account.balance_enquiry()}")
        print("----------------------")

    def print_transaction_history(self):
        for account in self.accounts:
            print(f"Account Type: {type(account).__name__}")
            transactions = account.get_transaction_history()
            for transaction in transactions:
                print(transaction)
            print("----------------------")

    def save_transaction_history(self):
        file_path = f"{self.username}_transaction_history.txt"
        with open(file_path, "w") as file:
            for account in self.accounts:
                transactions = account.get_transaction_history()
                file.write(f"Account Type: {type(account).__name__}\n")
                for transaction in transactions:
                    file.write(f"{transaction}\n")
                file.write("----------------------\n")
        print(f"Transaction history saved to '{file_path}'.")



class Admin:
    def __init__(self, banking_system):
        self.banking_system = banking_system

    def print_all_customer_balances(self):
        file_path = "customer_balances.txt"
        with open(file_path, "w") as file:
            for customer in self.banking_system.customers:
                file.write(f"Customer: {customer.username}\n")
                for account in customer.accounts:
                    file.write(f"Account Type: {type(account).__name__}, Balance: {account.balance_enquiry()}\n")
                file.write("----------------------\n")
        print(f"Customer balances saved to '{file_path}'.")

    def save_all_customer_transactions(self):
        for customer in self.banking_system.customers:
            customer.save_transaction_history()
        print("Transaction history saved for all customers.")


class BankingSystem:
    def __init__(self):
        self.customers = []

    def create_customer(self, username, password, first_name, last_name, address):
        customer = Customer(username, password, first_name, last_name, address)
        self.customers.append(customer)

    def get_customer_balance(self, username, account_type):
        for customer in self.customers:
            if customer.username == username:
                return customer.get_account_balance(account_type)
        return None


def display_customer_menu(customer):
    while True:
        print("\n1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Print Account Balances")
        print("5. Print Transaction History")
        print("6. Exit")
        option = input("Enter your option (1-6): ")

        if option == "1":
            account_type = input("Enter account type (Checking/Saving/Loan): ")
            if account_type == "Checking":
                balance = float(input("Enter initial balance: "))
                credit_limit = float(input("Enter credit limit: "))
                overdraft_fee = float(input("Enter overdraft fee: "))
                account = CheckingAccount(balance, credit_limit, overdraft_fee)
                customer.create_account(account)
                print("Checking account created successfully!")
            elif account_type == "Saving":
                balance = float(input("Enter initial balance: "))
                interest_rate = float(input("Enter interest rate: "))
                account = SavingAccount(balance, interest_rate)
                customer.create_account(account)
                print("Saving account created successfully!")
            elif account_type == "Loan":
                balance = float(input("Enter initial balance: "))
                principal_amount = float(input("Enter principal amount: "))
                interest_rate = float(input("Enter interest rate: "))
                loan_duration = int(input("Enter loan duration in months: "))
                account = LoanAccount(balance, principal_amount, interest_rate, loan_duration)
                customer.create_account(account)
                print("Loan account created successfully!")
            else:
                print("Invalid account type!")

        elif option == "2":
            account_type = input("Enter account type (Checking/Saving/Loan): ")
            amount = float(input("Enter amount to deposit: "))
            success = customer.deposit(get_account_class(account_type), amount)
            if success:
                print("Deposit successful!")
            else:
                print("Deposit failed!")

        elif option == "3":
            account_type = input("Enter account type (Checking/Saving/Loan): ")
            amount = float(input("Enter amount to withdraw: "))
            success = customer.withdraw(get_account_class(account_type), amount)
            if success:
                print("Withdrawal successful!")
            else:
                print("Withdrawal failed!")

        elif option == "4":
            customer.print_account_balances()

        elif option == "5":
            customer.print_transaction_history()

        elif option == "6":
            customer.save_transaction_history()
            print("Transaction history saved successfully!")
            break

        else:
            print("Invalid option!")


def display_admin_menu(admin):
    while True:
        print("\n1. Print All Customer Balances")
        print("2. Save Transaction History for All Customers")
        print("3. Exit")
        option = input("Enter your option (1-3): ")

        if option == "1":
            admin.print_all_customer_balances()

        elif option == "2":
            admin.save_all_customer_transactions()

        elif option == "3":
            break

        else:
            print("Invalid option!")


def get_account_class(account_type):
    if account_type == "Checking":
        return CheckingAccount
    elif account_type == "Saving":
        return SavingAccount
    elif account_type == "Loan":
        return LoanAccount
    else:
        return None


# Example usage:
banking_system = BankingSystem()

# Create customers
banking_system.create_customer("hadi", "pass", "Hadi", "Raza", "123 Main St")
banking_system.create_customer("alman", "pass", "Alman", "Raza", "456 Elm St")

# Access created customers
customer1 = banking_system.customers[0]
customer2 = banking_system.customers[1]

# Create accounts for customers
customer1.create_account(CheckingAccount(balance=1000, credit_limit=500, overdraft_fee=50))
customer1.create_account(SavingAccount(balance=5000, interest_rate=2.5))

customer2.create_account(CheckingAccount(balance=2000, credit_limit=1000, overdraft_fee=75))
customer2.create_account(LoanAccount(balance=5000, principal_amount=10000, interest_rate=5, loan_duration=12))

# Customer menu
while True:
    print("\n1. Customer Login")
    print("2. Admin Login")
    print("3. Exit")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")

        customer = None
        for c in banking_system.customers:
            if c.username == username and c.password == password:
                customer = c
                break

        if customer:
            display_customer_menu(customer)
        else:
            print("Invalid username or password!")

    elif choice == "2":
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        if username == "admin" and password == "admin123":
            admin = Admin(banking_system)
            display_admin_menu(admin)
        else:
            print("Invalid admin credentials!")

    elif choice == "3":
        break

    else:
        print("Invalid choice!")
