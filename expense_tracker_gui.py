import sys
import csv
from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog

print("Python version:", sys.version)
print("Starting script...")

def migrate_expense_file():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
            for i, expense in enumerate(expenses):
                if 'id' not in expense:
                    expense['id'] = str(i + 1)

        # Write the updated expenses back to the CSV file
        fieldnames = ['id', 'date', 'amount', 'category']
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expenses)
    except FileNotFoundError:
        print("No expenses.csv file found. Migration not needed.")

# Call this function once to migrate the existing CSV data
migrate_expense_file()

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Expense Tracker")
        master.geometry("600x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        print("Initializing ExpenseTrackerApp")

        self.expenses = self.load_expenses()

        # Date Entry
        date_label = ctk.CTkLabel(master, text="Date (YYYY-MM-DD):")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ctk.CTkEntry(master)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        # Amount Entry
        amount_label = ctk.CTkLabel(master, text="Amount (Rs):")
        amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ctk.CTkEntry(master)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category Entry
        category_label = ctk.CTkLabel(master, text="Category:")
        category_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = ctk.CTkEntry(master)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button Frame for horizontal layout
        button_frame = ctk.CTkFrame(master)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Add Expense Button
        add_button = ctk.CTkButton(button_frame, text="Add Expense", command=self.add_expense, width=10, height=30)
        add_button.grid(row=0, column=0, padx=5)

        # Delete Expense Button
        delete_button = ctk.CTkButton(button_frame, text="Delete Expense", command=self.delete_expense, width=10, height=30)
        delete_button.grid(row=0, column=1, padx=5)

        # Edit Expense Button
        edit_button = ctk.CTkButton(button_frame, text="Edit Expense", command=self.edit_expense, width=10, height=30)
        edit_button.grid(row=0, column=2, padx=5)

        # Search Expense Button
        search_button = ctk.CTkButton(button_frame, text="Search Expense", command=self.search_expense, width=10, height=30)
        search_button.grid(row=0, column=3, padx=5)

        # Expense List using CTkTextbox
        self.expense_tree = ctk.CTkTextbox(master, height=150, width=500)
        self.expense_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Total Expenses Label
        self.total_label = ctk.CTkLabel(master, text="Total Expenses: Rs 0.00")
        self.total_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.update_expense_list()
        self.update_total()

        print("ExpenseTrackerApp initialized")

    def load_expenses(self):
        try:
            with open('expenses.csv', 'r') as file:
                reader = csv.DictReader(file)
                expenses = list(reader)
                # Ensure each expense has an 'id' field
                for i, expense in enumerate(expenses):
                    if 'id' not in expense:
                        expense['id'] = str(i + 1)
                return expenses
        except FileNotFoundError:
            return []

    def save_expenses(self):
        fieldnames = ['id', 'date', 'amount', 'category']
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.expenses)

    def add_expense(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        new_expense = {
            'id': str(len(self.expenses) + 1),  # Unique identifier for each expense
            'date': date,
            'amount': amount,
            'category': category
        }

        self.expenses.append(new_expense)
        self.save_expenses()
        messagebox.showinfo("Success", "Expense added successfully!")
        self.update_expense_list()
        self.update_total()

    def delete_expense(self):
        self.update_expense_list()  # Refresh the list before deletion
        selected_index = self.ask_for_selection("delete")
        if selected_index is not None:
            expense_to_delete = self.expenses[selected_index]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the expense on {expense_to_delete['date']} for Rs {expense_to_delete['amount']} in category '{expense_to_delete['category']}'?"):
                del self.expenses[selected_index]
                self.save_expenses()
                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.update_expense_list()
                self.update_total()

    def edit_expense(self):
        self.update_expense_list()  # Refresh the list before editing
        selected_index = self.ask_for_selection("edit")
        if selected_index is not None:
            self.expense_to_edit_index = selected_index
            expense_to_edit = self.expenses[selected_index]
            
            # Pre-fill the fields with the selected expense details
            self.date_entry.delete(0, ctk.END)
            self.date_entry.insert(0, expense_to_edit['date'])
            self.amount_entry.delete(0, ctk.END)
            self.amount_entry.insert(0, expense_to_edit['amount'])
            self.category_entry.delete(0, ctk.END)
            self.category_entry.insert(0, expense_to_edit['category'])

            # Show a Save Changes button
            save_button = ctk.CTkButton(self.master, text="Save Changes", command=self.save_edited_expense, width=10, height=30)
            save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_edited_expense(self):
        new_date = self.date_entry.get()
        new_amount = self.amount_entry.get()
        new_category = self.category_entry.get()

        try:
            new_amount = float(new_amount)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        # Update the expense with new values
        self.expenses[self.expense_to_edit_index] = {
            'id': self.expenses[self.expense_to_edit_index]['id'],  # Keep the same ID
            'date': new_date,
            'amount': new_amount,
            'category': new_category
        }

        self.save_expenses()
        messagebox.showinfo("Success", "Expense edited successfully!")
        self.update_expense_list()
        self.update_total()

        # Clear the entry fields
        self.date_entry.delete(0, ctk.END)
        self.amount_entry.delete(0, ctk.END)
        self.category_entry.delete(0, ctk.END)

    def ask_for_selection(self, action):
        # Display the expenses with indices
        self.expense_tree.delete(1.0, ctk.END)
        for index, expense in enumerate(self.expenses):
            self.expense_tree.insert(ctk.END, f"{index}: Date: {expense['date']}, Amount: Rs {expense['amount']}, Category: {expense['category']}\n")

        # Ask user for the index of the expense to edit/delete
        index_input = simpledialog.askinteger("Select Expense", f"Enter the index of the expense to {action} (0-{len(self.expenses) - 1}):")
        
        if index_input is not None and 0 <= index_input < len(self.expenses):
            return index_input
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid index.")
            return None

    def search_expense(self):
        search_date = self.date_entry.get()
        search_results = [expense for expense in self.expenses if expense['date'] == search_date]
        
        self.expense_tree.delete(1.0, ctk.END)
        
        if search_results:
            total_for_date = sum(float(expense['amount']) for expense in search_results)
            self.expense_tree.insert(ctk.END, f"Expenses for {search_date}:\n")
            for expense in search_results:
                self.expense_tree.insert(ctk.END, f"Amount: Rs {expense['amount']}, Category: {expense['category']}\n")
            self.expense_tree.insert(ctk.END, f"\nTotal for {search_date}: Rs {total_for_date:.2f}")
        else:
            self.expense_tree.insert(ctk.END, f"No expenses found for {search_date}")

    def update_expense_list(self):
        self.expense_tree.delete(1.0, ctk.END)
        for expense in self.expenses:
            self.expense_tree.insert(ctk.END, f"Date: {expense['date']}, Amount: Rs {expense['amount']}, Category: {expense['category']}\n")

    def update_total(self):
        total = sum(float(expense['amount']) for expense in self.expenses)
        self.total_label.configure(text=f"Total Expenses: Rs {total:.2f}")

print("Defining root window")
root = ctk.CTk()
print("Creating ExpenseTrackerApp instance")
app = ExpenseTrackerApp(root)
print("Starting main event loop")
root.mainloop()
print("Main event loop ended")

