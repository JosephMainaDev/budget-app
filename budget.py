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
        if not self.check_funds(amount):
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
        if not self.check_funds(amount):
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

    def __str__(self):
        """
        String representation of this budget Category.
        
        The title line is 30 characters long with the budget Category name
        in the middle of "*"s

        Each item in the ledger is represented with a description and
        the amount. The description is 23 characters max. The amount is
        7 characters long max, has 2 decimal places and is right aligned.

        The total amount in the budget Category is displayed last.
        """
        f = (30 - len(self.category)) // 2
        t = "*" * f + self.category
        title = t + "*" * (30 - len(t)) + "\n"

        items = ""

        for obj in self.ledger:
            amount = "{:.2f}".format(obj["amount"])[:7]
            description = obj["description"][:23]
            items += description + amount.rjust(30 - len(description)) + "\n"

        total = "Total: " + "{:.2f}".format(self.get_balance())


        return title + items + total


def create_spend_chart(categories):
    """
    Creates a bar chart showing the percentage spent in each budget Category.

    The percentage spent is calculated by withdrawals.

    Argument:
        categories (list): Budget Category objects to show on the bar chart.
    
    Returns:
        string: The string representing the bar chart.
    """

    # The bar chart is made up of the following parts:
    bar_chart = []

    # [1] Title with a given string.
    title = "Percentage spent by category"
    bar_chart.append(title)
    
    # [2] Labels from 0 - 100 in steps of 10.
    # bars[] stores the top part of the chart (with labels and the percentages).
    bars = []
    labels = [(str(p) + "| ").rjust(5) for p in range(0, 110, 10)]
    labels.reverse()
    bars.append(labels)

    # [3] Bars whose height is a percentage of the amount spent (withdrawals).
    withdrawals = []
    for category in categories:
        withdrawn = 0
        for obj in category.ledger:
            if obj["amount"] < 0:
                withdrawn += obj["amount"]
        withdrawals.append(withdrawn)
    
    # Withdrawals as a percentage, rounded down to the nearest 10.
    percentages = [int(round(w / sum(withdrawals) * 100, -1)) for w in withdrawals]

    for p in percentages:
        # A bar is made up of o's for every 10%.
        bar = ["o  " for _ in range(0, p + 10, 10)]
        # Match len() of all bars to that of labels (easier to work with!).
        bar += ["   "] * (len(labels) - len(bar))
        bar.reverse()
        bars.append(bar)

    len_labels = len(labels)
    num_categories = len(categories)
    for i in range(len_labels):
        line = ""
        for j in range(num_categories + 1):
            #line += chart[j][i]
            line += bars[j][i]
        bar_chart.append(line)

    # [4] Horizontal line made up of dashes
    len_barchart_line = len(bar_chart[1])
    hor = ("-" * 3 * num_categories + "-").rjust(len_barchart_line)
    bar_chart.append(hor)

    # [5] Category names written vertically below the bars.
    names = [category.category for category in categories]
    longest_name = len(max(names, key=len))
    names = [name + " " * (longest_name - len(name)) for name in names]

    for i in range(longest_name):
        line = ""
        for j in range(num_categories):
            line += names[j][i] + "  "
        bar_chart.append(line.rjust(len_barchart_line))

    # Make the bar chart.
    return "\n".join(bar_chart)
