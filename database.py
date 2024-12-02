import sqlite3
from typing import List, Dict
from datetime import datetime
import os
import pandas as pd

def init_db():
    """Initialize the SQLite database"""
    # Check if database exists
    db_exists = os.path.exists('hackernews.db')
    
    conn = sqlite3.connect('hackernews.db')
    c = conn.cursor()
    
    if not db_exists:
        # Create new table with all columns
        c.execute('''
            CREATE TABLE articles
            (title TEXT, url TEXT, summary TEXT, 
             score INTEGER, timestamp INTEGER,
             content TEXT,  
             fetched_at DATETIME)
        ''')
    else:
        # Check if content column exists
        cursor = c.execute('PRAGMA table_info(articles)')
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add content column if it doesn't exist
        if 'content' not in columns:
            print("Adding 'content' column to existing database...")
            c.execute('ALTER TABLE articles ADD COLUMN content TEXT')
    
    conn.commit()
    conn.close()

def save_articles(articles: List[Dict]):
    """Save articles to the database"""
    conn = sqlite3.connect('hackernews.db')
    c = conn.cursor()
    
    for article in articles:
        c.execute('''
            INSERT INTO articles 
            (title, url, summary, score, timestamp, content, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            article['title'],
            article['url'],
            article['summary'],
            article['score'],
            article['timestamp'],
            article.get('content', ''),
            datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()
    
    # After saving to database, create Excel export
    export_to_excel(articles)

def export_to_excel(articles: List[Dict]):
    """Export articles to Excel file"""
    # Create a directory for exports if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    
    # Use a fixed filename instead of timestamp-based
    filename = 'exports/hackernews_summaries.xlsx'
    
    # Format the data for new articles
    new_data = []
    for article in articles:
        new_data.append({
            'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Title': article['title'],
            'URL': article['url'],
            'Summary': article['summary'],
            'Score': article['score']
        })
    
    new_df = pd.DataFrame(new_data)
    
    if os.path.exists(filename):
        # Read existing Excel file
        existing_df = pd.read_excel(filename)
        # Concatenate existing data with new data
        df = pd.concat([existing_df, new_df], ignore_index=True)
        print(f"\nAppending {len(new_data)} articles to existing Excel file: {filename}")
    else:
        df = new_df
        print(f"\nCreating new Excel file: {filename}")
    
    # Export to Excel with formatting
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Summaries')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Summaries']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 100)
    
    print(f"Excel file saved with {len(df)} total articles") 