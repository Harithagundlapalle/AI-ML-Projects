import os
import subprocess
import time
import json
import wikipedia
import webbrowser
import requests
import wolframalpha
import datetime
import pyttsx3
import speech_recognition as sr
print('LOADING YOUR PERSONAL A.I ASSISTANT JARVIS')
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice",'voices[0].id')
def speak(text):
    engine.say(text)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Haritha")
        print("Good Morning Haritha")
    elif hour>=12 and hour<16:
        speak("Good Afternoon Haritha")
        print("Good Afternoon Haritha")
    elif hour>=16 and hour<22:
        speak("Good Evening Haritha")
        print("Good Evening Haritha")
    else:
        speak("It's too late. You better go to sleep Sahil. Good Night")
        print("It's too late. You better go to sleep Sahil. Good Night")
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        statement = r.recognize_google(audio, language='en-in')
        print(f"User Said: {statement}\n")

    except Exception as e:
        print(e)
        print("Please can you say it again..")
        return "None"

    return statement
speak("LOADING YOUR PERSONAL AI ASSISTANT JARVIS")
wishMe()
if __name__ == '__main__':
    while True:
        speak("How can I help you?")
        statement = takeCommand().lower()
        if statement == 0:
            continue
        if "thank you" in statement or "stop" in statement:
            speak("Your Personal AI Assistant JARVIS is shutting down, GOOD BYE")
            print("Your Personal AI Assistant JARVIS is shutting down, GOOD BYE")
            break

        if 'wikipedia' in statement:
            speak("Searching Wikipedia...")
            print("Searching Wikipedia...")
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to wikipedia...")
            print(results)
            speak(results)

        elif "open youtube" in statement:
            speak("Opening Youtube")
            print("Opening Youtube")
            webbrowser.open_new_tab("https://www.youtube.com")
            time.sleep(5)

        elif "open google" in statement:
            speak("Opening google")
            print("Opening google")
            webbrowser.open_new_tab("https://www.google.com")
            time.sleep(5)

        elif "open gmail" in statement:
            speak("Opening gmail")
            print("Opening gmail")
            webbrowser.open_new_tab("https://mail.google.com")
            time.sleep(5)

        elif "weather" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = 'https://api.openweathermap.org/data/2.5/weather?'
            speak("What is the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak("the temperature in kelvin units is " + str(current_temperature) + "\nhumidity in percentage is" +
                      str(current_humidity) + "\n weather descripton" + str(weather_description))
                print("the temperature in kelvin units is " + str(current_temperature) + "\nhumidity in percentage is" +
                      str(current_humidity) + "\n weather descripton" + str(weather_description))
            else:
                speak("city not found")
                print("city not found")

        elif "time" in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is{strTime}")

        elif "who are you" in statement or "what can you do" in statement:
            speak(
                "Iam JARVIS. Your personal assistant. I can perform the following task like opening YouTube, Gmail, Google chrome and stack overflow. Also, I can Predict current time, take a photo, search Wikipedia to abstract required data, predict weather in different cities, get top headline news from Times of India and can answer computational and geographical questions too.")
            print(
                "Iam JARVIS. Your personal assistant. I can perform the following task like opening YouTube, Gmail, Google chrome and stack overflow. Also, I can Predict current time, take a photo, search Wikipedia to abstract required data, predict weather in different cities, get top headline news from Times of India and can answer computational and geographical questions too.")

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was made by Sahil")
            print("I was made by Sahil")

        elif "open stackoverflow" in statement:
            speak("Opening stack overflow")
            print("Opening stack overflow")
            webbrowser.open_new_tab("https://stackoverflow.com")
            time.sleep(5)

        elif "news" in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak("Here are some headlines from times of India for you")
            time.sleep(5)

        elif "search" in statement:
            statement = statement.replace("search", " ")
            webbrowser.open_new_tab("statement")
            time.sleep(5)

        elif "ask" in statement:
            speak(
                "My versions are still under upgradation progress to enable more cool features. But you can try asking me computational and geographical questions now. Sure, I will answer those. What do you want to ask?")
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif 'shutdown' in statement:
            if platform == "win32":
                os.system('shutdown /p /f')
            elif platform == "linux" or platform == "linux2" or "darwin":
                os.system('poweroff')

time.sleep(3)