from openai import OpenAI
from dotenv import load_dotenv
import pyperclip
from pynput import keyboard
import rumps
import json
from system import prompt

load_dotenv(override=True)

client = OpenAI()

class FunctionGPTApp(rumps.App):
    def __init__(self):
        super(FunctionGPTApp, self).__init__("X")
        self.menu = ["Press F1 to process clipboard"]
        self.keyboard_listener = None
        self.start_listener()
        self.tools = json.load(open('tools.json', 'r'))
    



    def start_listener(self):
        def on_press(key):
            if key == keyboard.Key.f1:
                messages = [{"role": "system", "content": prompt},
                            {"role": "user", "content": pyperclip.paste()}]
                answer = self.process_text(messages)
                self.title = answer[:50] + "..." if len(answer) > 50 else answer
            if key == keyboard.Key.f2:
                messages = [ {"role": "user", "content":  pyperclip.paste()}] 
                chat = client.chat.completions.create(model="gpt-4o", messages=messages)
                reply = chat.choices[0].message.content 
                print(reply)
                pyperclip.copy(reply)
        
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.keyboard_listener.start()

    def process_text(self, messages):
        try:
            chat = client.chat.completions.create(model="gpt-4o", messages=messages, temperature=0.3, tools=self.tools, tool_choice="required")
            if chat.choices[0].message.tool_calls:
                reply = chat.choices[0].message.tool_calls[0].function.arguments
                options = json.loads(reply)['options']
                return ','.join([f'{i}' for i in options])
            else:
                return chat.choices[0].message.content
        except Exception as e:
            self.title = "Error: " + str(e)[:50]
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    FunctionGPTApp().run()


