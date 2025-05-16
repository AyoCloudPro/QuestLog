from datetime import datetime
import requests
import random


# Greetings function
# =====================
def get_greeting():
    current_hour = datetime.now().hour
    if current_hour < 9:
        return "Rise and shine adventurer. Your quests await!"
    elif 9 <= current_hour < 12:
        return "Good morning brave warrior!"
    elif 12 <= current_hour < 18:
        return "Good afternoon hero, busy as ever i see!"
    else:
        return "Good evening, night owl. No rest for the wicked!"


# Random quotes function
# ======================
def get_random_quotes():
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            return f"{data['content']} — {data['author']}"
        else:
            return "Too hard, Too hurt, Too changed... " \
                   "if you're not too much of 'something' then you are not enough. - Senna, league of legends"
    except Exception:
        return "It's not about how much time you have, it's how you use it. - Ekko, league of legends"