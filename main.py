import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
from groq import Groq  # Assuming Groq is installed

def speak_text(text, lang="ko"):
    """Converts text to speech and plays the audio."""
    try:
        audio_file = os.path.abspath("output.mp3")
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)  # Delete audio file after playing
    except Exception as e:
        print("Error occurred:", e)

def listen_for_keyword():
    """Waits for the keyword 'hey bro' to activate the assistant."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for the keyword 'hey bro'...")
        speak_text("Say 'hey bro' to start GPT.")

        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language='en-US').lower()

                if "hey bro" in text:
                    print("Keyword 'hey bro' detected! Please speak in Korean.")
                    speak_text("Hello user, how can I help you?")
                    return  # Exit the loop when keyword is detected
            except sr.UnknownValueError:
                print("Speech not recognized, trying again...")
            except sr.RequestError:
                print("Google Speech Recognition service error.")

def listen_for_korean(groq_client):
    """Listens for Korean input and responds using Groq GPT."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                print("Listening for Korean input...")
                audio = recognizer.listen(source, timeout=10)
                korean_text = recognizer.recognize_google(audio, language='ko-KR')
                print(f"Recognized Korean: {korean_text}")

                gpt_response = groq_model(korean_text, groq_client)
                print(gpt_response)
                speak_text(gpt_response)

            except sr.WaitTimeoutError:
                print("No input detected for 10 seconds, returning to keyword mode.")
                speak_text("Returning to keyword mode due to inactivity.")
                return  # Return to keyword detection
            except sr.UnknownValueError:
                print("Could not recognize Korean input.")
                speak_text("I could not understand you, please try again.")
            except sr.RequestError:
                print("Google Speech Recognition service error.")
                speak_text("There is an issue with the speech recognition service.")

def groq_model(descriptions, groq_client):
    """Sends user input to Groq GPT model and returns the response."""
    try:
        file_content = "\n".join(descriptions)
        system_prompt = "Provide friendly and supportive responses to user queries."

        response = groq_client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": file_content}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Error in generating response."

if __name__ == "__main__":
    api_key_groq = "groq_api_key_here"
    groq_client = Groq(api_key=api_key_groq)

    while True:
        listen_for_keyword()  # Detect "hey bro"
        listen_for_korean(groq_client)  # Process Korean input and respond
