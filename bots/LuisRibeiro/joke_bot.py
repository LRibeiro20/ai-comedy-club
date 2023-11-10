import openai
import ast
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Bot:
    name = 'Luis'

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

    def tell_joke(self):
        messages = [
            {"role": "system", "content": 'You are a joke rater. Return response as json. {"rate": 6}'},
            {"role": "assistant", "content": '{"mood": "", "joke_preference": ""}'},
            {"role": "user", "content": "I'm feeling good today."},
        ]

        print("Bot: Hi there! How are you feeling today?")
        user_mood = input("You: ")
        messages.append({"role": "user", "content": user_mood})

        print("Bot: Great! What type of jokes do you prefer? (e.g., puns, dad jokes)")
        user_preference = input("You: ")
        messages[-2]['content'] = f'{{"mood": "{user_mood}", "joke_preference": "{user_preference}"}}'

        response = openai.Completion.create(
            model="text-davinci-002",  # Use a model capable of joke generation
            prompt=f'Tell me a {user_preference} joke:',
            max_tokens=150
        )

        assistant_message = response['choices'][0]['text'].strip()
        messages.append({"role": "assistant", "content": assistant_message})  # Append the assistant's response

        print(f"Bot: Here's a joke for you: {assistant_message}")

        return assistant_message

    def rate_joke(self, user_joke):
        messages = [
            {"role": "system", "content": 'You are a joke rater. Return response as json. {"rate": 6}'},
            {"role": "assistant", "content": '{"mood": "", "joke_preference": ""}'},
            {"role": "user", "content": "I'm feeling good today."},
            {"role": "assistant", "content": user_joke},
        ]

        joke_generated = False
        while not joke_generated:
            user_message = input("You: ")  # Get the user's input
            messages.append({"role": "user", "content": user_message})  # Append the user message

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )

            assistant_message = response['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": assistant_message})  # Append the assistant's response

            try:
                rating = ast.literal_eval(assistant_message)['rate']
                joke_generated = True
            except (KeyError, SyntaxError):
                print(f"Bot: {ast.literal_eval(assistant_message)['message']}")
                print("Bot: Can you tell me another joke to rate?")

        return rating

# Usage
bot = Bot()

# Tell a joke
joke = bot.tell_joke()

# Rate the joke
rating = bot.rate_joke(joke)
print(f"Rating for the joke: {rating}")
