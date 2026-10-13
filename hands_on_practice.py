class Student:
    """Represents a student with name, age, and grade attributes"""

    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def get_details(self):
        return f"Student: {self.name}, Age: {self.age}, Grade: {self.grade}"


class BankAccount:
    """Represents a bank account with deposit and withdraw operations"""

    def __init__(self, account_holder, initial_balance=0.0):
        self.account_holder = account_holder
        self.balance = float(initial_balance)

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be positive"
        self.balance += amount
        return True, f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be positive"
        if amount > self.balance:
            return False, "Insufficient funds"
        self.balance -= amount
        return True, f"Withdrew ${amount:.2f}. Remaining balance: ${self.balance:.2f}"


class PracticeBook:
    """Represents a book with title, author, and status properties"""

    def __init__(self, title, author, status="Available"):
        self.title = title
        self.author = author
        self._status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    def mark_borrowed(self):
        self._status = "Borrowed"

    def mark_available(self):
        self._status = "Available"


class Vehicle:
    """Base class for vehicles"""

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start_engine(self):
        return f"{self.year} {self.make} {self.model} engine started."

    def describe(self):
        return f"{self.year} {self.make} {self.model}"


class Car(Vehicle):
    """Car class inheriting from Vehicle"""

    def __init__(self, make, model, year, doors=4):
        super().__init__(make, model, year)
        self.doors = doors

    def drive(self):
        return f"Driving the {self.make} {self.model} on 4 wheels."


class Motorcycle(Vehicle):
    """Motorcycle class inheriting from Vehicle"""

    def __init__(self, make, model, year, has_sidecar=False):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

    def ride(self):
        return f"Riding the {self.make} {self.model} on 2 wheels."


def demonstrate_hands_on_practice():
    student1 = Student("Alice", 20, "A")
    student2 = Student("Bob", 22, "B+")
    print(student1.get_details())
    print(student2.get_details())

    account = BankAccount("Alice", 100.0)
    print(account.deposit(50.0)[1])
    print(account.withdraw(30.0)[1])

    book = PracticeBook("1984", "George Orwell")
    print(f"Book status: {book.status}")
    book.mark_borrowed()
    print(f"Updated book status: {book.status}")

    car1 = Car("Toyota", "Camry", 2022)
    car2 = Car("Honda", "Civic", 2021)
    moto = Motorcycle("Yamaha", "MT-07", 2023)

    print(car1.start_engine())
    print(car1.drive())
    print(car2.describe())
    print(moto.start_engine())
    print(moto.ride())


if __name__ == "__main__":
    demonstrate_hands_on_practice()
