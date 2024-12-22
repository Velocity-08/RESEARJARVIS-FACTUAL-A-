import spacy
import requests
from googlesearch import search
from bs4 import BeautifulSoup

# Load spaCy model for NER (Named Entity Recognition)
nlp = spacy.load("en_core_web_sm")

# Step 1: Understanding the Query
def process_query(query):
    # Process the query using spaCy
    doc = nlp(query)
    
    # Extract named entities (e.g., "planets," "Elon Musk")
    entities = [ent.text for ent in doc.ents]
    
    # Detect the type of question (e.g., 'who', 'how many', 'what is')
    if query.lower().startswith("who"):
        question_type = 'who'
    elif query.lower().startswith("how many"):
        question_type = 'how many'
    elif query.lower().startswith("what is"):
        question_type = 'what is'
    else:
        question_type = 'general'
    
    return {
        'entities': entities,
        'question_type': question_type
    }

# Step 2: Web Scraping
def web_search_and_scrape(query, num_results=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    scraped_data = []
    
    try:
        # Perform Google search
        search_results = search(query, num_results=num_results)
        
        for url in search_results:
            print(f"Scraping URL: {url}")
            
            try:
                # Send GET request with headers to bypass scraping restrictions
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()  # Will raise an exception for status codes 4xx or 5xx
                
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text content
                page_text = ' '.join(p.text for p in soup.find_all('p'))
                scraped_data.append({'url': url, 'content': page_text})
            
            except requests.exceptions.RequestException as e:
                print(f"Error accessing {url}: {e}")
    
    except Exception as e:
        print(f"Error during search: {e}")
    
    return scraped_data

# Step 3: Extract the Most Relevant Answer
def extract_relevant_answer(scraped_data, question_type):
    for item in scraped_data:
        content = item['content'].lower()
        
        # Simple matching based on question type
        if question_type == 'how many' and "planets" in content:
            if "8" in content:
                return "There are 8 planets in our solar system."
            elif "9" in content:
                return "There are 9 planets in our solar system, including Pluto."
        
        if question_type == 'who' and "elon musk" in content:
            if "elon musk" in content:
                return "Elon Musk is the CEO of SpaceX and Tesla."
        
        if question_type == 'what is' and "capital" in content:
            if "paris" in content:
                return "The capital of France is Paris."
    
    return "Sorry, I couldn't find the answer."

# Main Function
def answer_factual_question(query):
    # Step 1: Process the query
    processed_query = process_query(query)
    print(f"Processed Query: {processed_query}")
    
    # Step 2: Scrape relevant content from the web
    scraped_data = web_search_and_scrape(query)
    
    # Step 3: Extract the most relevant answer
    answer = extract_relevant_answer(scraped_data, processed_query['question_type'])
    print(f"Answer: {answer}")
    
    return answer

# Example usage
if __name__ == "__main__":
    query = input("Enter your search query: ")
    answer = answer_factual_question(query)
    print(f"Final Answer: {answer}")
