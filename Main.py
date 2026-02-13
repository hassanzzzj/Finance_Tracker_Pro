import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkcalendar import DateEntry
from tkinter import filedialog
from datetime import date


# System Settings
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class SignupWindow(ctk.CTkToplevel): # CTkToplevel for popup window
    def __init__(self, parent):
        super().__init__(parent)
        self.title("FinanceTracker - Create Account")
        self.geometry("450x600")
        
        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(master=self, corner_radius=20)
        self.main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.label = ctk.CTkLabel(master=self.main_frame, text="Create Account", font=("Roboto", 24, "bold"))
        self.label.pack(pady=(30, 10))

        # --- Inputs ---
        self.username_entry = ctk.CTkEntry(master=self.main_frame, width=250, placeholder_text="Choose Username")
        self.username_entry.pack(pady=12)

        self.password_entry = ctk.CTkEntry(master=self.main_frame, width=250, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12)

        self.confirm_password_entry = ctk.CTkEntry(master=self.main_frame, width=250, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.pack(pady=12)

        # --- Button: Register ---
        self.signup_button = ctk.CTkButton(master=self.main_frame, text="Sign Up", width=250,command=self.register_user, corner_radius=8, fg_color="green", hover_color="#006400")
        self.signup_button.pack(pady=(25, 12))

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conf_password = self.confirm_password_entry.get()

        if not username or not password:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        if password != conf_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            db = mysql.connector.connect(
                host="localhost", user="root", password="hassan123", database="finance_db"
            )
            cursor = db.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already taken!")
            else:
                # Insert new user
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                messagebox.showinfo("Success", "Account Created Successfully! You can now Login.")
                self.withdraw() # CLose signup window
                log_in = LoginApp()  
                log_in.mainloop() # Open login window
            
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"MySQL Error: {err}")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FinanceTracker Pro - Login")
        self.geometry("450x550")

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(master=self, corner_radius=20)
        self.main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        # --- Label: Welcome ---
        self.label = ctk.CTkLabel(master=self.main_frame, text="Welcome Back", 
                                  font=("Roboto", 24, "bold"))
        self.label.pack(pady=(30, 10))

        self.sub_label = ctk.CTkLabel(master=self.main_frame, text="Manage your wealth efficiently", 
                                      font=("Roboto", 12), text_color="gray")
        self.sub_label.pack(pady=(0, 30))

        # --- Input: Username ---
        self.username_entry = ctk.CTkEntry(master=self.main_frame, width=250, 
                                           placeholder_text="Username")
        self.username_entry.pack(pady=12)

        # --- Input: Password ---
        self.password_entry = ctk.CTkEntry(master=self.main_frame, width=250, 
                                           placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12)

        # --- Button: Login ---
        self.login_button = ctk.CTkButton(master=self.main_frame, text="Login", 
                                          width=250, command=self.login_event,
                                          corner_radius=8, font=("Roboto", 14, "bold"))
        self.login_button.pack(pady=(25, 12))

       

        # --- Label: Register Link ---
        self.signup_link = ctk.CTkButton(master=self.main_frame, text="New User? Create Account", 
                                 fg_color="transparent", text_color="gray", 
                                 hover_color=None, command=self.open_signup)
        self.signup_link.pack(pady=10)
      
    def open_signup(self):
        self.withdraw()  # close login window
        SignupWindow(self)
    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please fill all fields")
            return

        try:
            # MySQL Connection
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hassan123",
                database="finance_db"
            )
            cursor = db.cursor()
            
            # Query (SQL Injection se bachne ke liye parameterized query use karein)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0] # USer id at index 0
                username = user[1] # Username at index 1
                self.withdraw() # close login window
                dash = DashboardWindow(username, user_id) # open dashboard window with username and user_id
                dash.mainloop()     
            else:
                messagebox.showerror("Error", "Invalid Credentials")
            
            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"MySQL Error: {err}")



class DashboardWindow(ctk.CTk):
    def __init__(self, username, user_id):
        super().__init__()
        self.username = username
        self.user_id = user_id
        
        self.title(f"FinanceTracker Pro - {username}")
        self.geometry("1100x650")
        
        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="FINANCE\nTRACKER", font=("Roboto", 24, "bold")).pack(pady=30)

        ctk.CTkButton(self.sidebar, text="Refresh Data", command=self.refresh_dashboard).pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Add Transaction", command=self.open_add_transaction).pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(self.sidebar, text="Logout", fg_color="#922B21", command=self.quit).pack(side="bottom", fill="x", padx=20, pady=20)

        # Export Button in Sidebar
        self.btn_export = ctk.CTkButton(self.sidebar, text="Export CSV", fg_color="#D4AC0D", text_color="black",
                                command=self.open_export_window)
        self.btn_export.pack(fill="x", padx=20, pady=10)

        # --- MAIN CONTENT ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Stats Cards placeholders
        self.stats_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)
        
        # Chart placeholder
        self.chart_frame = ctk.CTkFrame(self.main_content, corner_radius=15)
        self.chart_frame.pack(fill="both", expand=True, pady=20)


        # Initial Load
        self.refresh_dashboard()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="hassan123", database="finance_db"
        )
    # --- EXPORT WINDOW ---
    def open_export_window(self):
        ExportWindow(self.user_id)

    def refresh_dashboard(self):
        """Database se data nikal kar UI update karna"""
        try:
            db = self.get_db_connection()
            cursor = db.cursor()

            # 1. Fetch Stats
            cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY type", (self.user_id,))
            results = dict(cursor.fetchall())
            
            income = float(results.get('Income', 0))
            expense = float(results.get('Expense', 0))
            balance = income - expense

            # Update Cards
            for widget in self.stats_frame.winfo_children(): widget.destroy()
            self.create_card(self.stats_frame, "Total Balance", f"Rs. {balance}", "#2E86C1").pack(side="left", padx=10, expand=True, fill="both")
            self.create_card(self.stats_frame, "Income", f"Rs. {income}", "#28B463").pack(side="left", padx=10, expand=True, fill="both")
            self.create_card(self.stats_frame, "Expenses", f"Rs. {expense}", "#CB4335").pack(side="left", padx=10, expand=True, fill="both")

            # 2. Fetch Chart Data
            cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = %s AND type = 'Expense' GROUP BY category", (self.user_id,))
            chart_data = cursor.fetchall()
            
            self.update_chart(chart_data)
            db.close()
        except Exception as e:
            print(f"Error: {e}")

    def create_card(self, parent, title, amount, color):
        card = ctk.CTkFrame(parent, corner_radius=15, border_width=2, border_color=color)
        ctk.CTkLabel(card, text=title, font=("Roboto", 14)).pack(pady=(15, 0))
        ctk.CTkLabel(card, text=amount, font=("Roboto", 22, "bold"), text_color=color).pack(pady=(5, 15))
        return card

    def update_chart(self, data):
        for widget in self.chart_frame.winfo_children(): widget.destroy()
        
        if not data:
            ctk.CTkLabel(self.chart_frame, text="No expense data to show").pack(pady=50)
            return

        categories = [x[0] for x in data]
        amounts = [float(x[1]) for x in data]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', textprops={'color':"w"})
        ax.set_title("Expense Breakdown", color="w")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

    def open_add_transaction(self):
        AddTransactionWindow(self.user_id, self.refresh_dashboard)

class AddTransactionWindow(ctk.CTkToplevel):
    def __init__(self, user_id, callback):
        super().__init__()
        self.user_id = user_id
        self.callback = callback
        self.geometry("400x500")
        self.title("Add New Entry")
        self.attributes('-topmost', True) # Window ko top par rakhne ke liye

        ctk.CTkLabel(self, text="New Transaction", font=("Roboto", 20, "bold")).pack(pady=20)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Enter Amount", width=250)
        self.amount_entry.pack(pady=10)

        self.category_opt = ctk.CTkOptionMenu(self, values=["Food", "Rent", "Bills", "Salary", "Shopping", "Others"], width=250)
        self.category_opt.pack(pady=10)

        self.type_opt = ctk.CTkOptionMenu(self, values=["Income", "Expense"], width=250)
        self.type_opt.pack(pady=10)

        ctk.CTkButton(self, text="Save Entry", command=self.save_to_db, width=250, fg_color="green").pack(pady=30)

    def save_to_db(self):
        amount = self.amount_entry.get()
        category = self.category_opt.get()
        t_type = self.type_opt.get()

        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="hassan123", database="finance_db")
            cursor = db.cursor()
            cursor.execute("INSERT INTO transactions (user_id, amount, category, type) VALUES (%s, %s, %s, %s)", (self.user_id, amount, category, t_type))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Transaction Saved!")
            self.callback() # Refresh dashboard
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

class ExportWindow(ctk.CTkToplevel):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.title("Export Transactions")
        self.geometry("400x450")
        self.attributes('-topmost', True)

        ctk.CTkLabel(self, text="Select Date Range", font=("Roboto", 22, "bold")).pack(pady=20)

        # --- Start Date Selection ---
        ctk.CTkLabel(self, text="Start Date:", font=("Roboto", 14)).pack(pady=(10, 5))
        self.start_cal = DateEntry(self, width=20, background='darkblue', 
                                   foreground='white', borderwidth=2, 
                                   date_pattern='yyyy-mm-dd')
        self.start_cal.pack(pady=5)

        # --- End Date Selection ---
        ctk.CTkLabel(self, text="End Date:", font=("Roboto", 14)).pack(pady=(20, 5))
        self.end_cal = DateEntry(self, width=20, background='darkblue', 
                                 foreground='white', borderwidth=2, 
                                 date_pattern='yyyy-mm-dd')
        self.end_cal.pack(pady=5)

        # --- Export Button ---
        self.export_btn = ctk.CTkButton(self, text="Download CSV Report", 
                                        fg_color="#28B463", hover_color="#1E8449",
                                        command=self.export_data, corner_radius=10)
        self.export_btn.pack(pady=40)

    def export_data(self):
        # access selected dates
        s_date = self.start_cal.get_date() # datetim.date object
        e_date = self.end_cal.get_date()

        if s_date > e_date:
            messagebox.showerror("Invalid Date", "Start date must be before end date!")
            return

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="hassan123", database="finance_db")
            
            query = """
                SELECT date, amount, category, type 
                FROM transactions 
                WHERE user_id = %s AND DATE(date) BETWEEN %s AND %s
            """
            
            # Pandas read_sql logic
            df = pd.read_sql(query, db, params=(self.user_id, s_date, e_date))

            if df.empty:
                messagebox.showwarning("No Data", "No transactions found in the selected date range.")
                return

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                     filetypes=[("CSV files", "*.csv")],
                                                     title="Save Report")
            
            if file_path:
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"File Saved successfully!\nPath: {file_path}")
                self.destroy()

            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
if __name__ == "__main__":
    app = LoginApp()  # Example user_id and username
    app.mainloop()