# AI-Assistant

----
## Prerequisites
Python 3.9 installed
  ```bash
  pip install SpeechRecognition gTTS playsound
  ```
----

```python
text = recognizer.recognize_google(audio, language='en-US')
```
Supported Language [Google Speech-to-Text](https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages)

----

```python
if __name__ == "__main__":
    api_key_groq = "groq_api_key_here" # change the api key in here
    groq_client = Groq(api_key=api_key_groq)
```

## How to start ? 
```python
python main.py
```
