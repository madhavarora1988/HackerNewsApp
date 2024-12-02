import requests
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"

def summarize_articles(articles: List[Dict]) -> List[Dict]:
    """Generate summaries for articles using local Ollama server running Llama model"""
    
    print("\n=== Generating Summaries using Ollama ===")
    
    for i, article in enumerate(articles, 1):
        prompt = f"""Please provide a brief 2-3 sentence summary of this article.
Title: {article['title']}
Content: {article['content']}"""
        
        print(f"\n{i}. Processing Article: {article['title']}")
        print(f"\n--- Full Prompt being sent to Ollama ---")
        print(prompt)
        print("----------------------------------------")
        print(f"   Sending to Ollama for summarization...")
        
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": "llama3.2:3b-instruct-q4_K_M",
                "prompt": prompt,
                "system": "You are a helpful assistant that provides brief, informative summaries of technical articles. Focus on the main points and key takeaways.",
                "stream": False
            })
            
            if response.status_code == 200:
                article['summary'] = response.json()['response']
                print(f"\n   Summary received: {article['summary']}")
            else:
                error_msg = f"Error: Failed to get response from Ollama server. Status code: {response.status_code}"
                article['summary'] = error_msg
                print(f"   {error_msg}")
                
        except Exception as e:
            error_msg = f"Error generating summary: {str(e)}"
            article['summary'] = error_msg
            print(f"   {error_msg}")
        
    return articles 