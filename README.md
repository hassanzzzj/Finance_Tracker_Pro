# FinanceTracker Pro 💹

FinanceTracker Pro is a high-performance, modern desktop application designed to help individuals manage their daily finances, track expenses, and visualize their spending habits. Built with Python and MySQL, it offers a secure and intuitive interface for personal wealth management.

## ✨ Key Features

* **Secure Authentication:** User registration and login system with password protection.
* **Dynamic Dashboard:** Real-time overview of Total Balance, Total Income, and Total Expenses.
* **Visual Analytics:** Interactive Pie Charts powered by Matplotlib to show expense breakdowns by category.
* **Transaction Management:** Quickly add income or expense entries with categorized tags (Food, Rent, Salary, etc.).
* **Data Export:** Export your financial reports into **CSV format** based on custom date ranges.
* **Modern UI:** A sleek, dark-themed interface built using the `CustomTkinter` library.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Library:** CustomTkinter
* **Database:** MySQL
* **Data Processing:** Pandas
* **Visualization:** Matplotlib
* **Utilities:** TkCalendar (for date selection)

## 🚀 Getting Started

### Prerequisites

1.  **Python Installed:** Ensure you have Python 3.7+ installed.
2.  **MySQL Server:** You need a running MySQL instance.
3.  **Database Setup:** Create a database named `finance_db` and the following tables:

```sql
CREATE DATABASE finance_db;

USE finance_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    category VARCHAR(50),
    type ENUM('Income', 'Expense'),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);