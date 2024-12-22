import speech_recognition as sr

def listen_continuously():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening continuously... Speak now!")
        
        while True:
            try:
                # Listen for a phrase (real-time chunking)
                print("Listening...")
                audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                
                # Convert speech to text
                query = recognizer.recognize_google(audio_data)
                print(f"You said: {query}")
            
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand the audio.")
            
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")
                break  # Exit on API failure
            
            except KeyboardInterrupt:
                print("\nStopped listening.")
                break  # Exit on user interrupt (Ctrl+C)

# Run the function to listen continuously
if __name__ == "__main__":
    listen_continuously()
