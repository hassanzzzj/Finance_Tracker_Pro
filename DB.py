import mysql.connector
def setup_mysql():
    try:
        # Apne MySQL credentials yahan likhein
        db = mysql.connector.connect(
            host="localhost",
            user="root",      # Default user 'root' hota hai
            password="hassan123"       # Agar koi password rakha hai to wo likhein
        )
        cursor = db.cursor()
        
        # Database banana
        cursor.execute("CREATE DATABASE IF NOT EXISTS finance_db")
        cursor.execute("USE finance_db")
        
        # Users Table banana
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        
        # Admin user check karna aur add karna
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('admin', '1234'))
            db.commit()
            
        print("MySQL Database and Table ready!")
        db.close()
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")

if __name__ == "__main__":
    setup_mysql()

# Transaction Table has be done manually by user in MySQL cli:

# CREATE TABLE IF NOT EXISTS transactions (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     amount DECIMAL(10, 2),
#     category VARCHAR(50),
#     type ENUM('Income', 'Expense'),
#     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );