from openai import OpenAI
from dotenv import load_dotenv
import pyperclip
from pynput import keyboard

load_dotenv(override=True)

client = OpenAI()

def on_press(key):
    if key == keyboard.Key.f1:  
        messages = [ {"role": "user", "content":  
              pyperclip.paste()} ] 
        updated_text = perform_function(messages)
        pyperclip.copy(updated_text)

def perform_function(messages):
    chat = client.chat.completions.create(model="gpt-4o", messages=messages)
    reply = chat.choices[0].message.content 
    return reply

with keyboard.Listener(on_press=on_press) as listener:
    print("Running...")
    listener.join()



