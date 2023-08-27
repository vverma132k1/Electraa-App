

# importing modules.
import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import urllib.parse
import requests
from gtts import gTTS
import time

# to chat one to one with the user.
chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

# to make the AI write things for us and put that text into a file so that it can be used later on.
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)


# this is used make the MAC OS voice speaker speak things.
# this can be altered too to someone else's voice.
def say(text):
    os.system(f'say "{text}"')

# this is used to give commands to the computer using the microphone as the source.
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Pardon, can you please repeat?"

def get_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=in&category=sports&pagesize=5&apiKey={api_key}"
    response = requests.get(url) # make a get request.
    news = response.json()    # Parse the response as JSON
    return [(article['title']) for article in news['articles']]


def speak_news(news):
    for title in news:
        print(title)  # print the news title
        tts = gTTS(text=title, lang='en')  # create gTTS object
        tts.save('news.mp3')  # save audio file
        os.system('mpg123 news.mp3')  # play audio file


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params) # make get request.
    weather = response.json()# make JSON of the response and store it in weather.

    main_weather = weather['weather'][0]['description']
    temperature = weather['main']['temp']
    city_name = weather['name']

    # Return a dictionary containing the weather data
    return {
        'city': city_name,
        'weather': main_weather,
        'temperature': temperature
    }

# this will return the formatted string of the information.
def format_weather(weather_info):
    return f"The current weather in {weather_info['city']} is {weather_info['weather']} with a temperature of {weather_info['temperature']}°C"


def parse_time_input(query):
    # Split the query into individual words
    words = query.split()

    # Look for a number in the query and extract it
    for word in words:
        if word.isdigit():
            return int(word)

    # If no number is found, return None (or a default value if desired)
    return None

def set_timer(seconds):
    say(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    say("Time's up!")


# this is the driver code.
if __name__ == '__main__':
    print('Welcome to Electraa')
    say("Welcome to Electraa, How can I help you?")

    # to infinitely listen to the user's commands.
    while True:
        print("Listening...")
        query = takeCommand()

    # making a list of lists called sites.
        sites = [
            ["youtube", "https://www.youtube.com/results?search_query="],
            ["wikipedia", "https://www.wikipedia.org/wiki/"],
            ["google", "https://www.google.com/search?q="],
            ["flipkart", "https://www.flipkart.com/search?q="],
            ["amazon", "https://www.amazon.com/s?k="],
            ["alibaba", "https://www.alibaba.com/trade/search?SearchText="]
        ]

        for site in sites:
            site_name = site[0]
            site_url = site[1]
            if f"open {site_name}".lower() in query.lower():
                # Extracting the query after the site name
                # this "split" will divide the query into two parts, till this "for" word ends
                # so now we have two parts of the query, so 0th will be the "open" till "for" and then 1st "websitename" that you give after "for".
                # strip is used to remove and white spaces.
                search_query = query.lower().split(f"open {site_name} and search for")[1].strip()
                say(f"Opening {site_name} sir...")
                # Encode the search query string into a proper URL format
                search_query_encoded = urllib.parse.quote_plus(search_query)
                # Open the website with the search query
                webbrowser.open(f"{site_url}{search_query_encoded}")

# getting the time information.
        if "the time" in query or "what time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} hours")
            say(f"and {min} minutes")

# opening applications
        elif "facetime" in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "notes" in query.lower():
            os.system(f"open /System/Applications/Notes.app")

        elif "mail" in query.lower():
            os.system(f"open /System/Applications/Mail.app")

        elif "whatsapp" in query.lower():
            os.system(f"open /Applications/whatsapp.app")

        elif "photos" in query.lower():
            os.system(f"open /System/Applications/Photos.app")

# quiting the electraa
        elif "quit" in query.lower() or "electra quit" in query.lower() or "stop listening" in query.lower() or "elektra quit" in query.lower():
            exit()

# to set the timer
        elif "timer" in query.lower():
            duration = parse_time_input(query)
            if duration is not None:
                set_timer(duration)
            else:
                say("Sorry, I couldn't understand the timer duration from your input.")

# to get news
        elif "news" in query.lower():
            api_key = 'e173a5925bc5408b98590a14b7791e45'
            news = get_news(api_key)
            # print(news)

            # Open a text file in write mode. This will create the file if it doesn't exist
            with open('news.txt', 'w') as f:
                # Write each title to the file on a new line
                for title in news:
                    f.write(title + '\n')

            speak_news(news)

        elif "weather" in query.lower():
            api_key = "ff49af37158127181835b19fc1d533ee"
            city = "delhi"  # Replace with your city
            weather_info = get_weather(api_key, city)
            print(format_weather(weather_info))

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else: # elif "hey listen".lower() in query.lower():
            print("Chatting...")
            chat(query)

