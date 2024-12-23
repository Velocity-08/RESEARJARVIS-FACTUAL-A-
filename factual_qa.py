import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# NewsAPI Function to fetch latest news based on the query
def fetch_latest_news(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # Extracting top news article
        articles = data.get('articles', [])
        if articles:
            title = articles[0]['title']
            description = articles[0]['description']
            url = articles[0]['url']
            return f"Latest news: {title} - {description}. Read more at {url}"
        else:
            return "No news articles found."
    else:
        return "Error fetching news."

# Google Search Function to fetch search results
def fetch_google_results(query):
    """
    Fetches Google search results for a given query.
    Returns a list of dictionaries with title, link, and snippet.
    """
    query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        results = []
        for g in soup.select(".tF2Cxc"):
            title = g.select_one(".DKV0Md").text
            link = g.select_one(".yuRUbf a")["href"]
            snippet = g.select_one(".VwiC3b").text if g.select_one(".VwiC3b") else "No description available"
            results.append({"title": title, "link": link, "snippet": snippet})
        return results
    else:
        print(f"Failed to fetch results: {response.status_code}")
        return []

# Function to fetch and summarize page content from the top Google result
def fetch_page_content(url):
    """
    Fetches and extracts text content from a given URL.
    Returns the combined text of all paragraphs on the page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all("p")
        content = " ".join([para.text for para in paragraphs])
        return content
    else:
        print(f"Failed to fetch content: {response.status_code}")
        return None

# Summarize the fetched content using Hugging Face Transformers
def summarize_text(content):
    """
    Summarizes the provided text using Hugging Face Transformers.
    Returns a summarized version of the text.
    """
    summarizer = pipeline("summarization")
    summary = summarizer(content, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Main function to answer factual questions
def answer_factual_question(query, api_key=None):
    """
    Combines both NewsAPI and Google search scraping based on the query type.
    If the question is about real-time events (e.g., current president), fetch news.
    Otherwise, perform a Google search to fetch information from relevant pages.
    """
    print(f"Question: {query}\n")

    # Check if the query relates to real-time news (e.g., "current president")
    if "current president" in query.lower():
        if api_key:
            # Fetch real-time news if NewsAPI key is provided
            news = fetch_latest_news("current president of the USA", api_key)
            print(news)
        else:
            print("News API key not provided.")
    else:
        # Otherwise, use Google search and scraping
        results = fetch_google_results(query)
        if not results:
            print("No results found.")
            return
        
        # Print search results
        print("Top Search Results:")
        for i, result in enumerate(results[:3], 1):  # Show top 3 results
            print(f"{i}. {result['title']}\n   {result['link']}\n   {result['snippet']}\n")

        # Fetch and summarize content from the top result
        top_result_url = results[0]["link"]
        print(f"Fetching content from: {top_result_url}\n")
        content = fetch_page_content(top_result_url)

        if content:
            print("Summarizing content...\n")
            summary = summarize_text(content[:2000])  # Limit content length for summarization
            print(f"Answer: {summary}\n")
        else:
            print("Failed to fetch content from the top result.")

# Example Usage
if __name__ == "__main__":
    # For testing purposes, provide a NewsAPI key for real-time data
    api_key = '892dac80a5474aa0a4deae8f7f484dc6'  # Replace with your actual NewsAPI key
    query = input("Enter your question: ")
    answer_factual_question(query, api_key)
