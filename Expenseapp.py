import csv
from datetime import datetime

# Function to load expenses from CSV file
def load_expenses():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

# Function to save expenses to CSV file
def save_expenses(expenses):
    fieldnames = ['date', 'amount', 'category']
    with open('expenses.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

# Load existing expenses
expenses = load_expenses()

def add_expense(date, amount, category):
    expenses.append({'date': date, 'amount': amount, 'category': category})
    save_expenses(expenses)
    print("Expense added successfully!")

def view_expenses():
    if not expenses:
        print("No expenses recorded yet.")
    else:
        for expense in expenses:
            print(f"Date: {expense['date']}, Amount: Rs {expense['amount']}, Category: {expense['category']}")

def search_expenses(search_term):
    results = [exp for exp in expenses if search_term.lower() in exp['date'].lower() or search_term.lower() in exp['category'].lower()]
    if not results:
        print("No matching expenses found.")
    else:
        for expense in results:
            print(f"Date: {expense['date']}, Amount: Rs {expense['amount']}, Category: {expense['category']}")

def main():
    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            amount = input("Enter amount spent : Rs ")
            category = input("Enter category: ")
            add_expense(date, amount, category)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            search_term = input("Enter date or category to search: ")
            search_expenses(search_term)
        elif choice == '4':
            print("Thank you for using the Expense Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()