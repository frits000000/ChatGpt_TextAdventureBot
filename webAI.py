from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import speech_recognition as sr
from gtts import gTTS
import os, datetime, time
import glob
import playsound
from pygame import mixer
from pydub import AudioSegment
import random
import subprocess
import keyboard

def send_prompt(driver, prompt, index):
    try:
        # Wait for the textarea to be present
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )

        # Send the prompt
        textarea.send_keys(prompt)

        # Find the send button and click it
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.flex.h-8.w-8.items-center.justify-center.rounded-full.bg-black.text-white"))
        )
        send_button.click()

        # Wait for response
        time.sleep(10)  # Adjust this as needed depending on the response time

        # Find all conversation turn elements with the specified class
        conversation_turns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".w-full.text-token-text-primary"))
        )

        # Check if there are enough conversation turns
        if len(conversation_turns) >= index + 1:
            # Get the conversation turn element at the specified index
            conversation_turn = conversation_turns[index]

            # Now, you can perform actions on the conversation turn element as needed
            # For example, you can extract text or perform further actions within this element
            # Example: text-message
            response_container = WebDriverWait(conversation_turn, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".text-message"))
            )

            response_paragraphs = response_container.find_elements(By.CSS_SELECTOR, "p")
            response_text = "\n".join(paragraph.text for paragraph in response_paragraphs)

            first_messgase = response_text

            response_container = WebDriverWait(conversation_turn, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".text-message"))
            )

            response_paragraphs = response_container.find_elements(By.CSS_SELECTOR, "p")
            response_text = "\n".join(paragraph.text for paragraph in response_paragraphs)

            

            while first_messgase != response_text:
                first_messgase = response_text

                time.sleep(5)
                
                response_container = WebDriverWait(conversation_turn, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".text-message"))
                )

                response_paragraphs = response_container.find_elements(By.CSS_SELECTOR, "p")
                response_text = "\n".join(paragraph.text for paragraph in response_paragraphs)

                

            return response_text

    except Exception as e:
        print("An error occurred:", e)


def listen_for_trigger(trigger_phrase="hello"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for trigger...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        if trigger_phrase.lower() in text.lower():
            return True
        else:
            return False
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return False
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return False

def capture_and_convert():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        while True:
            print("Press T to speak or y to type")
            if keyboard.is_pressed('t'):
                print("Listening... Speak something:")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = recognizer.listen(source)
                break
            if keyboard.is_pressed('y'):
                print("Type your message:")
                # Prompt the user to type something
                user_input = input("Type something: ")

                return user_input

    try:
        print("Recognizing...")
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

def speed_swifter(sound, speed=1):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    return sound_with_altered_frame_rate

def say(frase):
    if os.path.exists("oldsound.mp3"):
        try:
            os.remove("oldsound.mp3")
        except Exception as e:
            time.sleep(0)
    if os.path.exists("newsound.mp3"):
        try:
            os.remove("newsound.mp3")
        except Exception as e:
            time.sleep(0)

    voz = gTTS(frase, lang='en', tld='us', slow=False).save("oldsound.mp3")
    mixer.init()
    mixer.music.load("oldsound.mp3")
    mixer.music.play()

    try:
        sound = AudioSegment.from_file("oldsound.mp3")    
        speed_sound = speed_swifter(sound)
        speed_sound.export(os.path.join("newsound.mp3"), format="mp3")
        mixer.init()
        mixer.music.load("newsound.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(e)


def text_to_speech(text):
    try:
        filename = "abc.mp3"
        tts = gTTS(text=text, lang='en', tld='co.in')
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("Error occurred during text-to-speech conversion or playback:", e)


def load_personalities(filename="personalities.txt"):
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except Exception as e:
        print("Error loading personalities:", e)
        return ""

def main():
    print("Welcome to ChatGPT! Type 'exit' to end the conversation.")
    driver = webdriver.Firefox()
    try:
        # Navigate to the ChatGPT website
        driver.get("https://www.chatgpt.com/")

        # Prompt user to log in
        input("Please log in to https://www.chatgpt.com/ in the browser window that just opened. Press Enter when you're done...")

        first_prompt = False
        index = 1  # Start with index 1

        inventory_info = ""
        health_info = ""
        
        while True:
            # Load personalities from file
            Personalities = load_personalities()

            trigger_detected = True
            while not trigger_detected:
                trigger_detected = listen_for_trigger()

            # Capture and convert speech
            user_input = capture_and_convert()

            print('text detected')

            while user_input == "":
                user_input = capture_and_convert()


            if user_input == "switch persona":
                prompt = Personalities + user_input


            if first_prompt == False:
                prompt = Personalities + user_input
                first_prompt = True
            
            else:
                prompt = user_input + " My current health is: " + health_info + ". In my inventory i have: " + inventory_info

            response = send_prompt(driver, prompt, index)

            # Construct the shell command
            #command = f"ponysay --balloon round '{response}'"

            # Execute the command
            #subprocess.run(command, shell=True)
            
            # Find the index of "Health:" and "Inventory:"
            health_index = response.find("Health:")
            inventory_index = response.find("Inventory:")

            # Extract values after "Health:" and "Inventory:" based on their indexes
            health_info = response[health_index + len("Health:"):inventory_index].strip()
            inventory_info = response[inventory_index + len("Inventory:"):].strip()

            say(response)

            index += 2  # Increment index by 2 for the next message

            # Listen for trigger phrase to continue
            continue_listening = False
            while not continue_listening:
                continue_listening = True
    finally:
        # Close the browser window
        driver.quit()

if __name__ == "__main__":
    main()

