import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Step 1: Fetch Google Search Results
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

# Step 2: Fetch Content from a Web Page
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

# Step 3: Summarize Extracted Content
def summarize_text(content):
    """
    Summarizes the provided text using Hugging Face Transformers.
    Returns a summarized version of the text.
    """
    summarizer = pipeline("summarization")
    summary = summarizer(content, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Step 4: Main Function
def answer_factual_question(query):
    """
    Combines all steps to answer a factual question.
    - Fetches search results.
    - Extracts content from the top result.
    - Summarizes the extracted content.
    """
    print(f"Question: {query}\n")
    
    # Fetch search results
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
    query = input("Enter your question: ")
    answer_factual_question(query)
