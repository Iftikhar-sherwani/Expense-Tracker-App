import sys
import csv
from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

print("Python version:", sys.version)
print("Starting script...")

class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Expense Tracker")
        master.geometry("500x400")
        ctk.set_appearance_mode("System")  # Set the appearance mode
        ctk.set_default_color_theme("blue")  # Set the default color theme

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

        # Add Expense Button
        add_button = ctk.CTkButton(master, text="Add Expense", command=self.add_expense)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Expense List using CTkTextbox
        self.expense_tree = ctk.CTkTextbox(master, height=150, width=400)  # Adjust height and width as needed
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
                return list(reader)
        except FileNotFoundError:
            return []

    def save_expenses(self):
        fieldnames = ['date', 'amount', 'category']
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
            amount = float(amount)  # Convert amount to float
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        # Append the new expense to the list
        self.expenses.append({'date': date, 'amount': amount, 'category': category})
        
        # Save the expenses to the CSV file
        self.save_expenses()
        
        # Show success message
        messagebox.showinfo("Success", "Expense added successfully!")
        
        # Update the display area with the new expense
        self.update_expense_list()
        self.update_total()

    def update_expense_list(self):
        # Clear the current contents of the display area
        self.expense_tree.delete(1.0, ctk.END)  # Clear the textbox
        for expense in self.expenses:
            self.expense_tree.insert(ctk.END, f"Date: {expense['date']}, Amount: Rs {expense['amount']}, Category: {expense['category']}\n")

    def update_total(self):
        total = sum(float(expense['amount']) for expense in self.expenses)
        self.total_label.configure(text=f"Total Expenses: Rs {total:.2f}")

print("Defining root window")
root = ctk.CTk()  # Use customtkinter root
print("Creating ExpenseTrackerApp instance")
app = ExpenseTrackerApp(root)
print("Starting main event loop")
root.mainloop()
print("Main event loop ended")