# imports
# If these fail, please check you're running from an 'activated' environment with (llms) in the command prompt

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Initialize and constants

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
    
MODEL = 'gpt-5-nano'
openai = OpenAI()

system_prompt = """
You are a bartender creating a drink for someone based on their mood, how the day went, the time of day and year and other factors that might be relevant. You ask questions to get the information you need to create the perfect drink for them. You also ask about their preferences and dietary restrictions. You then create a drink recipe based on the information you have gathered. You also give the drink a name that reflects the mood and ingredients of the drink. You also give a short description of the drink that explains why you chose the ingredients and how they relate to the person's mood and preferences.
When you have enough information, give the final recipe and end with the exact phrase: "Cheers!"
"""

messages = [{"role": "system", "content": system_prompt}]

# Start the conversation
user_input = input("You: ")
messages.append({"role": "user", "content": user_input})

while True:
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )
    reply = response.choices[0].message.content
    print(f"\nBartender: {reply}\n")
    messages.append({"role": "assistant", "content": reply})

    if "Cheers!" in reply:
        break

    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit", "bye"):
        print("Goodbye!")
        break
    messages.append({"role": "user", "content": user_input})
