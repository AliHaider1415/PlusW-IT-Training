import os 
import glob 
import shutil 
import pandas as pd
import sqlite3
import yfinance as yf
import time
import requests
from bs4 import BeautifulSoup

def export_data(df, filename, format): 
    if format == "csv": 
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename} in CSV format.") 
    elif format == "json":
        df.to_json(filename, orient="records")
        print(f"Data exported to {filename} in JSON format.") 
    else: print("Unsupported format.")

def move_csv_file(file_name, folder_name):
    shutil.move(file_name, folder_name)
    print(f"File: {file_name} moved to {folder_name}")


# Creating a sample dataframe 
data = {'Name': ['Alice', 'Bob', 'Charlie'], 
        'Age': [25, 30, 35], 
        'City': ['New York', 'Los Angeles', 'Chicago']}

df = pd.DataFrame(data)

# Exporting to CSV 
export_data(df, "output1.csv", "csv")
export_data(df, "output2.csv", "csv")
export_data(df, "output3.csv", "csv")

move_csv_file("output1.csv", "backup_folder/")
move_csv_file("output2.csv", "backup_folder/")
move_csv_file("output3.csv", "backup_folder/")


# Database setup
db_name = "stocks.db"
conn = sqlite3.connect(db_name, check_same_thread=False)  # Allow multithreading
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    )
''')
conn.commit()

# Function to fetch stock data
def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d", interval="1m")  # 1-day history, 1-minute interval
        
        if data.empty:
            print(f"No data found for {symbol}. Skipping...")
            return None  # Return None if no data is available

        latest = data.iloc[-1]  # Get the most recent price data

        return {
            "symbol": symbol,
            "open": latest["Open"],
            "high": latest["High"],
            "low": latest["Low"],
            "close": latest["Close"],
            "volume": latest["Volume"]
        }
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Function to store data in SQLite
def store_data(symbol):
    stock_data = fetch_stock_data(symbol)
    
    if stock_data:  # Only store if data is available
        try:
            cursor.execute('''
                INSERT INTO stock_data (symbol, open, high, low, close, volume) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                stock_data["symbol"], stock_data["open"], stock_data["high"],
                stock_data["low"], stock_data["close"], stock_data["volume"]
            ))
            conn.commit()
            print(f"Stored data for {symbol}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

# Function to analyze stock data
def analyze_stock(symbol):
    try:
        df = pd.read_sql_query(
            "SELECT * FROM stock_data WHERE symbol=? ORDER BY timestamp DESC LIMIT 100", 
            conn, 
            params=(symbol,)
        )
        print(df)
    except Exception as e:
        print(f"Error analyzing stock data for {symbol}: {e}")

# Example Usage
if __name__ == "__main__":
    symbol = "AAPL"  # Apple stock
    
    for _ in range(5):  # Fetch data 5 times with intervals
        store_data(symbol)
        time.sleep(60)  # Wait for 1 minute before fetching again

    analyze_stock(symbol)

    # Close database connection
    conn.close()


# Target website
URL = "https://www.aljazeera.com/news/"

# Headers for request
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Function to scrape books
def get_books(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        book_list = []

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            stock = book.find("p", class_="instock availability").text.strip()

            book_list.append({
                "Title": title,
                "Price": price,
                "Availability": stock
            })

        return book_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Scrape book data
books_data = get_books(URL)

# Convert to DataFrame and save to CSV
if books_data:
    df = pd.DataFrame(books_data)
    df.to_csv("books.csv", index=False)
    print("Data saved to books.csv")
else:
    print("No data scraped.")
