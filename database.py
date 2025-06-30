#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
from datetime import datetime
import os

class OliveOilDatabase:
    def __init__(self, db_path="olive_oil.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                year INTEGER NOT NULL,
                type TEXT NOT NULL,
                sales REAL NOT NULL,
                volume REAL NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table for future multi-user support
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create analysis_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL,
                parameters TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_data_from_csv(self, csv_path="olive_oil_data.csv"):
        """Load data from CSV into database"""
        if not os.path.exists(csv_path):
            return False
        
        # Ensure tables exist before loading
        self.init_database()
        
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(self.db_path)
        
        # Clear existing data to avoid duplicates on reload
        conn.execute("DELETE FROM sales")
        
        # Insert new data
        df.to_sql('sales', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()
        return True
    
    def get_all_data(self):
        """Get all sales data"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        conn.close()
        return df
    
    def add_sale(self, country, year, type_oil, sales, volume, price):
        """Add a new sale record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sales (country, year, type, sales, volume, price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (country, year, type_oil, sales, volume, price))
        
        conn.commit()
        conn.close()
    
    def update_sale(self, sale_id, country, year, type_oil, sales, volume, price):
        """Update an existing sale record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sales 
            SET country=?, year=?, type=?, sales=?, volume=?, price=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (country, year, type_oil, sales, volume, price, sale_id))
        
        conn.commit()
        conn.close()
    
    def delete_sale(self, sale_id):
        """Delete a sale record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sales WHERE id=?", (sale_id,))
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, analysis_type, parameters, result):
        """Save analysis results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_history (analysis_type, parameters, result)
            VALUES (?, ?, ?)
        ''', (analysis_type, str(parameters), str(result)))
        
        conn.commit()
        conn.close()
    
    def get_analysis_history(self, limit=10):
        """Get recent analysis history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analysis_history 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_statistics(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total records
        cursor.execute("SELECT COUNT(*) FROM sales")
        total_records = cursor.fetchone()[0]
        
        # Total sales
        cursor.execute("SELECT SUM(sales) FROM sales")
        total_sales = cursor.fetchone()[0] or 0
        
        # Countries count
        cursor.execute("SELECT COUNT(DISTINCT country) FROM sales")
        countries_count = cursor.fetchone()[0]
        
        # Years range
        cursor.execute("SELECT MIN(year), MAX(year) FROM sales")
        year_range = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_records': total_records,
            'total_sales': total_sales,
            'countries_count': countries_count,
            'year_range': year_range
        }

# Global database instance
db = OliveOilDatabase() 