import requests
from bs4 import BeautifulSoup

# Function to scrape BBC News
def fetch_bbc_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # Find headlines from the main news section
        headlines = soup.find_all("h3", class_="gs-c-promo-heading__title")
        if headlines:
            return [headline.text.strip() for headline in headlines[:5]]  # Get top 5 headlines
        else:
            return "No news found."
    else:
        return "Failed to fetch BBC News."

# Function to scrape CNN News
def fetch_cnn_news():
    url = "https://edition.cnn.com/world"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # Find headlines from the main news section
        headlines = soup.find_all("span", class_="cd__headline-text")
        if headlines:
            return [headline.text.strip() for headline in headlines[:5]]  # Get top 5 headlines
        else:
            return "No news found."
    else:
        return "Failed to fetch CNN News."

# Function to scrape Reuters News
def fetch_reuters_news():
    url = "https://www.reuters.com"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # Find headlines from the main news section
        headlines = soup.find_all("h3", class_="story-title")
        if headlines:
            return [headline.text.strip() for headline in headlines[:5]]  # Get top 5 headlines
        else:
            return "No news found."
    else:
        return "Failed to fetch Reuters News."

# Main function to fetch real-time news from major sources
def fetch_real_time_news(query):
    print(f"Searching for real-time news related to: {query}\n")
    
    if "breaking news" in query.lower() or "current affairs" in query.lower() or "news" in query.lower():
        bbc_news = fetch_bbc_news()
        cnn_news = fetch_cnn_news()
        reuters_news = fetch_reuters_news()

        print("BBC News:")
        print("\n".join(bbc_news))
        print("\nCNN News:")
        print("\n".join(cnn_news))
        print("\nReuters News:")
        print("\n".join(reuters_news))
    else:
        print("This is not a real-time news query. Please ask about breaking news or current affairs.")

# Example Usage
if __name__ == "__main__":
    query = input("Enter your question (e.g., 'breaking news', 'current affairs', 'news'): ")
    fetch_real_time_news(query)
