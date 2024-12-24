import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline

# Time-related queries
def get_current_time():
    return f"The current time is: {datetime.now().strftime('%H:%M:%S')}"

# IMDb API Integration
def fetch_movie_details(movie_name):
    api_key = "af5f2122"  # Replace with your IMDb API key
    url = f"https://imdb-api.com/en/API/SearchMovie/{api_key}/{movie_name}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data.get("results"):
        movie = data["results"][0]
        return f"Movie: {movie['title']}\nDescription: {movie['description']}\nMore Info: {movie['id']}"
    return "Movie not found or error in IMDb API."

# OpenWeatherMap Integration
def fetch_weather(city_name):
    api_key = "230e150b75b34da0c1e7fbd73f7784e4"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city_name} is {weather} with a temperature of {temp}°C."
    return "City not found or error in OpenWeatherMap API."

# Wikipedia API Integration
def fetch_wikipedia_summary(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary available.") + f"\nRead more: {data.get('content_urls', {}).get('desktop', {}).get('page', '')}"
    return "Topic not found on Wikipedia."

# Google Search Integration
def fetch_google_results(query):
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
    return []

# Wolfram Alpha API Integration
def fetch_wolfram_alpha(query):
    app_id = "Y7ELP3-HQV9P3AV42"  
    url = f"http://api.wolframalpha.com/v2/query?input={query}&format=plaintext&output=JSON&appid={app_id}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data.get("queryresult"):
        pods = data["queryresult"].get("pods", [])
        answers = []
        for pod in pods:
            if "subpod" in pod:
                answers.append(pod["subpod"][0].get("plaintext", "No answer found"))
        return "\n".join(answers)
    return "No results found in Wolfram Alpha."

# Finnhub API Integration (Stock Market Data)
def fetch_stock_data_finnhub(stock_symbol):
    api_key = "ctlcfupr01qv7qq1tk60ctlcfupr01qv7qq1tk6g"  # Replace with your Finnhub API key
    url = f"https://finnhub.io/api/v1/quote?symbol={stock_symbol}&token={api_key}"
    response = requests.get(url)
    data = response.json()

    # Check if the data is valid
    if "c" in data:
        current_price = data["c"]  # Current price
        high_price = data["h"]  # High price
        low_price = data["l"]  # Low price
        open_price = data["o"]  # Open price
        return f"Stock data for {stock_symbol}:\nCurrent: {current_price}\nHigh: {high_price}\nLow: {low_price}\nOpen: {open_price}"
    else:
        return f"Could not retrieve stock data for {stock_symbol}. Please check the ticker symbol or try again later."

# NewsAPI Function to fetch latest news
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

# Function to fetch and summarize page content from the top Google result
def fetch_page_content(url):
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
    summarizer = pipeline("summarization")
    summary = summarizer(content, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Main function for handling user questions
def answer_question(question, api_key=None):
    if "time" in question.lower():
        return get_current_time()
    elif "weather" in question.lower():
        city = question.split("in")[-1].strip()
        return fetch_weather(city)
    elif "movie" in question.lower():
        movie = question.split("about")[-1].strip()
        return fetch_movie_details(movie)
    elif "wikipedia" in question.lower():
        topic = question.split("wikipedia")[-1].strip()
        return fetch_wikipedia_summary(topic)
    elif "wolfram" in question.lower() or "math" in question.lower():
        return fetch_wolfram_alpha(question)
    elif "stock" in question.lower() or "market" in question.lower():
        stock_symbol = question.split("for")[-1].strip()
        return fetch_stock_data_finnhub(stock_symbol)
    elif "news" in question.lower():
        if api_key:
            return fetch_latest_news(" ".join(question.split()[1:]), api_key)
        else:
            return "News API key not provided."
    else:
        results = fetch_google_results(question)
        if not results:
            return "No results found."
        
        # Fetch and summarize content from the top result
        top_result_url = results[0]["link"]  # Extract the link from the top result
        content = fetch_page_content(top_result_url)
        if content:
            return summarize_text(content[:2000])
        else:
            return "Failed to fetch content from the top result."

# Example Usage
if __name__ == "__main__":
    api_key = '892dac80a5474aa0a4deae8f7f484dc6'  # Replace with your actual NewsAPI key
    while True:
        question = input("Enter your question (or type 'exit' to quit): ")
        if question.lower() == "exit":
            print("Goodbye!")
            break
        print("\n" + answer_question(question, api_key) + "\n")
