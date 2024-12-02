import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from hn_fetcher import fetch_top_stories
from article_summarizer import summarize_articles
from database import init_db, save_articles

load_dotenv()

def main():
    print("HackerNews Summary App Started!")
    
    # Delete existing database if it exists
    if os.path.exists('hackernews.db'):
        print("Removing old database...")
        os.remove('hackernews.db')
    
    # Initialize the database
    init_db()
    
    def fetch_and_summarize():
        print(f"\nFetching articles at {datetime.now()}")
        articles = fetch_top_stories(limit=10)  # Get top 10 stories
        articles_with_summaries = summarize_articles(articles)
        save_articles(articles_with_summaries)
        print("Articles fetched, summarized and saved!")
        
        # Print the latest articles
        for article in articles_with_summaries:
            print(f"\nTitle: {article['title']}")
            print(f"URL: {article['url']}")
            print(f"Summary: {article['summary']}")
            print("-" * 50)

    # Schedule the job to run daily at 9 AM
    schedule.every().day.at("09:00").do(fetch_and_summarize)
    
    # Run once immediately when starting
    fetch_and_summarize()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
