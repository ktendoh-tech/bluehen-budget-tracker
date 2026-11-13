from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

set_website_title("Blue Hen Budget Tracker & Planner")
set_site_information(
    author="Kenan",
    description="Is a budget planner and tracker that allows for students to track their spending and saving by setting goals ",
    sources="",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/ktendoh-tech/bluehen-budget-tracker"]
)
hide_debug_information()
set_website_framed(False)


@dataclass
class Transaction:
    description: str
    amount: float
    category: str
    transaction_type: str
    date: str

@dataclass
class State:
    transactions: list[Transaction]
    monthly_budget: float
    savings_goal: float
    search_query: str
    selected_category: str
    total_savings: float
    balance: float
    

#routes
 
@route
def home(state: State)-> Page:
    """
    Is the homepage of the program which shows all information about the user's savings, balance, goals, and budget
    Args:
    state (State): is the current state of the program which stores the current the state of every attribute in the dataclass
    Returns:
           Page: returns a page with every attribute and its current information listed
    """
    return Page(state, [
        Text("Student Budget Planner"),
        Text("Income, Expenses, and Savings"),
        Text("Monthly Budget: $" + str(state.monthly_budget)),
        Text("Savings: $" + str(state.savings_goal)),
        Text("Balance: $" + str(state.balance)),
        Button("View Transactions", "user_transactions"),
        Button("Add Transaction", "add_transaction"),
        Button("Monthly Budget", "user_budget"),
        Button("My Savings", "user_savings"),
        Button("Search by Category", "search_category"),
        Button("Search Transactions", "search_transaction")
    ])


@route
def add_transaction(state: State)-> Page:
    """
    Lets the user add and stores a transaction
    
    Args:
        state (State): is the arg that represents the State dataclass that is the current state
        
    Returns:
           Page: returns a page that includes input boxes that the user uses to input information
    """
    return Page(state, [
        Text("Description of transaction: "),
             TextBox("current_description", ""),
        
        Text("Amount : "),
             TextBox("current_amount", ""),
        
        Text("Category: "),
             TextBox("current_category", ""),
        
        Text("Transaction type: "),
             SelectBox("type_choice", ["Income", "Expense"], "Expense"),
        
        Text("Date: "),
             TextBox("date", ""),
        
        "\n",
        Button("Submit", "list_user_transactions")
    ])

#Unit Tests
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)

assert_equal(add_transaction(state).state, state)
assert_equal(type(add_transaction(state)), Page)
assert_equal(state.transactions, [])


@route
def list_user_transactions(state: State,
                          current_description: str,
                          current_amount: str,
                          current_category: str,
                          type_choice: str,
                          date: str) -> Page:
    """
    Lists all the transactions the user has added
       
    Args:
         state (State): is the current state of the program and is the State dataclasses
         current_description (str): is the current description of a transaction
         current_category (str): is the current category of a transaction
         type_choice: is the current type of transaction
         date: is the date of transaction
           
    Returns:
           Page: returns a page of all the listed user transactions
           
    """

    amount = float(current_amount)
    new_transaction = Transaction(current_description, amount, current_category, type_choice, date)
    state.transactions.append(new_transaction)
    
    if type_choice == "Income":
        state.balance += amount
    else:
        state.balance -= amount
        
    page_content = [
    Text("Transaction added!"),
    Text("Updated Balance: $" + str(state.balance))
]
    for transaction in state.transactions:
        page_content.append(Text(transaction.description + " " + str(transaction.amount) + " " + transaction.category + " " + transaction.transaction_type + " " + transaction.date))
            
    return Page(state, page_content)

#Unit test
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)

result = list_user_transactions(state, "Paycheck", "1000", "Work", "Income", "11/13/2026")
assert_equal(state.balance, 1000.0)


@route
def user_transactions(state: State) -> Page:
    """
    Represents all the user transactions
    
    Args:
        state (State): is the current state
        
    Returns:
           Page: returns a page of all transactions
    """
    transaction_content = [Text("Your Transactions")]
    for transaction in state.transactions:
        transaction_content.append(Text(
    transaction.description + " $" +
    str(transaction.amount) + " " +
    transaction.category + " " +
    transaction.transaction_type + " " +
    transaction.date
))
    if not state.transactions:
        return Page(state, [
            Text("No Transactions")
        ])
    
    return Page(state, transaction_content)

#user_transactions unit test

state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)
result = user_transactions(state)
assert_equal(result.content, [Text("No Transactions")])

state = State(
    [Transaction("Paycheck", 1000.0, "Work", "Income", "11/13/2026")],
    500.0, 1000.0, "", "", 0.0, 1000.0
)
result = user_transactions(state)
assert_equal(len(state.transactions), 1)

state = State(
    [
        Transaction("Paycheck", 1000.0, "Work", "Income", "11/13/2026"),
        Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026")
    ],
    500.0, 1000.0, "", "", 0.0, 950.0
)
result = user_transactions(state)
assert_equal(len(state.transactions), 2)
        
      
            
@route
def user_budget(state: State) -> Page:
    """
    Shows the current budget that was set by the user
    
    Args:
        state (State): is the current state of the programs that stores the current budget set
        
    Returns:
           Page: returns a page with the current budget and allows for the user to change it if needed
        
    """
    return Page(state, [
        Text("Set Your Monthly Budget"),
        Text("Enter your monthly budget:"),
        TextBox("new_budget", ""),
        Button("Submit Budget", "update_budget")
    ])

# user_budget Unit tests
#Test 1
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)
result = user_budget(state)
assert_equal(result.state, state)

#Test 2
state = State([], 750.0, 1000.0, "", "", 0.0, 0.0)
result = user_budget(state)
assert_equal(result.state.monthly_budget, 750.0)

#Test 3
state = State([], 1200.0, 1000.0, "", "", 0.0, 0.0)
result = user_budget(state)
assert_equal(type(result), Page)


@route
def update_budget(state: State, new_budget: float)-> Page:
    """
    Updates the budget when the user decides to set a new budget
    
    Args:
        state (State): is the current state of the program that stores the current budget set
        new_budget (float): represents the new budget that the user wants to set
        
    Returns:
           Page: returns a page which shows and confirms that the budget has been updated
    """
    amount = float(new_budget)
    state.monthly_budget = amount
    return Page(state, [
        Text("Budget updated"),
        Text("Updated budget: $" + str(state.monthly_budget)),
    ])

#update_budget unit tests
#Test 1
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)
result = update_budget(state, 750.0)
assert_equal(state.monthly_budget, 750.0)

#Test 2
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)
result = update_budget(state, 1200.0)
assert_equal(state.monthly_budget, 1200.0)

#Test 3
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)
result = update_budget(state, 300.0)
assert_equal(state.monthly_budget, 300.0)


@route
def user_savings(state: State) -> Page:
    """
    Displays the savings and savings goals that the user has
    
    Args:
        state (State): is the current state of the program which stores the current savings and savings goals
        
    Returns:
           Page: returns a page that displays the user's savings and goals which can be updated
    """
    return Page(state, [
        Text("My Savings"),
        Text("Total Savings: $" + str(state.total_savings)),
        Text("Savings Goal: $" + str(state.savings_goal)),
        Text("Enter your current savings:"),
        TextBox("new_savings", ""),
        Text("Enter your savings goal:"),
        TextBox("new_goal", ""),
        Button("Update Savings", "update_savings")
    ])

#user_savings Unit tests
#Test 1
state = State([], 500.0, 1000.0, "", "", 250.0, 0.0)
result = user_savings(state)
assert_equal(state.total_savings, 250.0)

#Test 2
state = State([], 500.0, 1000.0, "", "", 500.0, 0.0)
result = user_savings(state)
assert_equal(state.savings_goal, 1000.0)

#Test 3
state = State([], 500.0, 1500.0, "", "", 750.0, 0.0)
result = user_savings(state)
assert_equal(state.total_savings, 750.0)


@route
def update_savings(state: State, new_savings: str, new_goal: str)-> Page:
    """
    Updates savings and goals after the user enters a new amount
    
    Args:
        state (State): is the current state of the program which stores the current savings and savings_goals
        new_savings (str): is the new amount the user has set for their savings
        new_goal (str): is the new goal that the user has set
    Returns:
           Page: returns a page of the new updated savings and goals which calculates if that goal was meant by the user's total savings
    """
    
    amount = float(new_savings)
    updated_savings_goal = float(new_goal)
  
    state.savings_goal = updated_savings_goal
    state.total_savings = amount
    
    if state.total_savings >= state.savings_goal:
        message = "You have reached your goal"
    else:
        message = "You are $ " + str(state.savings_goal - state.total_savings) + "away from reaching your current goal"
        
    return Page(state, [
    Text("Total Savings: $" + str(state.total_savings)),
    Text("Savings Goal: $" + str(state.savings_goal)),
    Text(message)
])

#update_savings Unit Tests
#Test 1
state = State([], 500.0, 1000.0, "", "", 200.0, 0.0)
result = update_savings(state, "500", "1000")
assert_equal(state.total_savings, 500.0)

#Test 2
state = State([], 500.0, 1000.0, "", "", 200.0, 0.0)
result = update_savings(state, "1000", "1000")
assert_equal(state.savings_goal, 1000.0)

#Test 3
state = State([], 500.0, 1500.0, "", "", 200.0, 0.0)
result = update_savings(state, "750", "1500")
assert_equal(state.total_savings, 750.0)


@route
def search_category(state: State) -> Page:
    """
    Allows for the user to search and filter a specific category that holds a list of transactions falling under that category
    
    Args:
        state (State): is the current state of the program that stores a list of transactions and its categories
    Returns:
           Page: Returns a page with a textbox allowing for the user to search and getting their results back
    """
    
    return Page(state, [
        Text("Search Transactions by Category"),
        Text("Enter a category:"),
        TextBox("category_search", ""),
        Button("Search", "display_search_category")
    ])

#search_category Unit tests
#Test 1
state = State([], 500.0, 1000.0, "", "", 0.0, 0.0)
result = search_category(state)
assert_equal(state.transactions, [])

#Test 2
state = State(
    [Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026")],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = search_category(state)
assert_equal(len(state.transactions), 1)


@route
def display_search_category(state: State, category_search: str)-> Page:
    """
    Displays all the transactions that fall under the category that the user searched
    
    Args:
        state (State): is the current state of the program that store the current trasnactions and its caregories
        category_search (str): is the category the user inputs to search for specific transactions
    Returns:
           Page: is a page that returns the results of what the user searched
    """
    category_list = [Text("Search Results:")]
    for transaction in state.transactions:
        if category_search == transaction.category:
            category_list.append(Text(
    transaction.description + " $" +
    str(transaction.amount) + " " +
    transaction.category + " " +
    transaction.transaction_type + " " +
    transaction.date
))
    return Page(state, category_list)

#display_search_category Unit Tests
state = State(
    [
        Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026"),
        Transaction("Restaurant", 30.0, "Food", "Expense", "11/13/2026"),
        Transaction("Textbook", 75.0, "Education", "Expense", "11/13/2026")
    ],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = display_search_category(state, "Food")
assert_equal(len(state.transactions), 3)


@route
def search_transaction(state: State) -> Page:
    """
    Allows for the user to search for a specific transaction by its attributes
    
    Args:
        state (State): is the current state of the program that stores a list of transactions and its attributes
    Returns:
           Page: Returns a page with a textbox allowing for the user to search and getting their results back
    """
    return Page(state, [
        Text("Search Transactions"),
        Text("Enter transaction description:"),
        TextBox("transaction_search", ""),
        Button("Search", "display_search_transaction")
    ])

#search_transaction Unit Tests
#Test 1
state = State(
    [Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026")],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = search_transaction(state)
assert_equal(len(state.transactions), 1)

#Test 2
state = State(
    [
        Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026"),
        Transaction("Paycheck", 1000.0, "Work", "Income", "11/13/2026")
    ],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = search_transaction(state)
assert_equal(len(state.transactions), 2)



@route
def display_search_transaction(state: State, transaction_search: str)-> Page:
    """
    Displays all the transaction that the user searched
    
    Args:
        state (State): is the current state of the program that store the current trasnactions and its attributes
        transaction_search (str): is the specific attribute the user inputs to search for specific transactions
    Returns:
           Page: is a page that returns the results of what the user searched
    """
    transaction_content_list = []
    for transaction in state.transactions:
        if transaction_search == transaction.description or transaction_search == transaction.date or transaction_search == str(transaction.amount):
            transaction_content_list.append(Text(
                transaction.description + " $" +
                str(transaction.amount) + " " +
                transaction.category + " " +
                transaction.transaction_type + " " +
                transaction.date
))
            
    if not transaction_content_list:
        return Page(state, [
            Text("Transaction not found")
        ])
    return Page(state, transaction_content_list)
    
#Unit Tests
#Test 1
state = State(
    [Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026")],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = display_search_transaction(state, "Groceries")
assert_equal(len(state.transactions), 1)

#Test 2
state = State(
    [Transaction("Paycheck", 1000.0, "Work", "Income", "11/13/2026")],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = display_search_transaction(state, "1000.0")
assert_equal(len(state.transactions), 1)

#Test 3
state = State(
    [
        Transaction("Groceries", 50.0, "Food", "Expense", "11/13/2026"),
        Transaction("Paycheck", 1000.0, "Work", "Income", "11/13/2026")
    ],
    500.0, 1000.0, "", "", 0.0, 0.0
)
result = display_search_transaction(state, "11/13/2026")
assert_equal(len(state.transactions), 2)




start_server(State(transactions=[], monthly_budget=0.0, savings_goal=0.0, search_query="", selected_category="", total_savings=0.0, balance=0.0))        
        
            


