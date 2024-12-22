import spacy

# Load the English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

def process_query(query):
    # Analyze the query using spaCy
    doc = nlp(query)
    
    # Extract the main intent (question type)
    intent = "Unknown"
    if query.lower().startswith(("what", "who", "where", "when", "why", "how")):
        intent = query.split()[0].capitalize()
    
    # Extract named entities (like proper nouns, dates, etc.)
    entities = {ent.text: ent.label_ for ent in doc.ents}
    
    # Extract important keywords (nouns, verbs)
    keywords = [token.text for token in doc if token.is_alpha and token.pos_ in ("NOUN", "VERB")]
    
    return intent, entities, keywords

# Example usage
if __name__ == "__main__":
    print("Enter your question:")
    user_query = input("> ")
    intent, entities, keywords = process_query(user_query)
    
    print(f"Intent: {intent}")
    print(f"Entities: {entities}")
    print(f"Keywords: {keywords}")
