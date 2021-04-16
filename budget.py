class Category:
    """
    Creates different budget categories.

    When objects are created, they are passed in the name of the category.
    For instance, food, clothing and entertainment.

    Attributes:
        category (str): The category of the Budget object.
    """

    def __init__(self, category):
        """
        Initialises the budget Category object with the passed in `category`.

        Argument:
            category (str): The category of the Budget object.
        """
        self.category = category
        self.ledger = []
    
    def deposit(self, amount, description = ""):
        """
        Appends an object to the ledger representing the amount deposited.

        The format of the object appended to the ledger is:
            {"amount": amount, "description": description}

        Arguments:
            amount (float): The amount of money to deposit.
            description (str): Describes the amount deposited.
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = ""):
        """
        Appends an object to the ledger representing the amount withdrawn.

        The format of the object appended to the ledger is:
            {"amount": -amount, "description": description}

        Arguments:
            amount (float): The amount of money to withdraw.
            description (str): Describes the amount withdrawn.

        Returns:
            bool: True if a withdrawal took place, False otherwise.
        """
        if not self.check_funds():
            return False

        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        """
        Computes the current balance in the budget Category.

        The balance is based on the deposits and withdrawals that have occured on
        the budget Category.Category

        Returns:
            float: The current balance.
        """
        return sum([obj["amount"] for obj in self.ledger])

    def transfer(self, amount, category):
        """
        Transfers `amount` from this budget Category to another `category`.

        The `amount` to be transferred is added as a withdrawal in this budget Category
        with a description of "Transfer to `category`". And it is deposited in the
        other `category` with a description of "Transfer from `category`".

        Arguments"
            amount (float): The amount to transfer.
            category (obj): A budget Category object to receive the amount transferred.

        Returns:
            bool: True if the transfer took place, False otherwise.
        """
        if not self.check_funds():
            return False

        # Withdraw from this Category and transfer to `category`
        self.withdraw(amount, "Transfer to " + category.category)

        # Deposit to `category` from this Category
        category.deposit(amount, "Transfer from " + self.category)

        return True
    
    def check_funds(self, amount):
        """
        Checks whether there is enough balance in the budget Category.

        It is used by both the withdraw and transfer methods.

        Argument:
            amount (float): The amount to check from the ledger.

        Returns:
            bool: False if the `amount` is greater than the balance in the budget
            Category, True otherwise.
        """
        if amount > self.get_balance():
            return False
        
        return True


def create_spend_chart(categories):
    pass