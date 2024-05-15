# ChatGpt_TextAdventureBot
 A python script to play your own text adventure using chat gpt and your mic or keyboard.
 The script is not perfect but works fine enough for a first upload, if needed i will document this script better.


## Before you start
install python on your system with the requirements in the requirements.txt.
intall firefox on your system.
You also need a open ai chatgpt account to use this script, no api keys needed since it interfaces with the web version of chat gpt


## Some info
The script tells you what key presses to use but let me briefly explain it to you:

Upon starting the script it will open the login page of chat gpt, use your credentials to log in and hit enter when focusing on the terminal window to proceed.

After you have two options pressing T will capture you audio so you can make a spoken prompt pressing y will open a text input for you to type your prompt. This precedure will repeat upon following prompts

The Script will then read the message of chat gpt and read it to you using tts.


## Info on the personalities.txt
within this file is the first prompt that will be inserted at your first prompt to chat gpt to make sure he behaves like we want it to. You can alter this to you own likings but there is one thing you need to keep in there.

In the file i tell the ai to add at the bottom of every message the health and the inventory of the user. You can alter this a bit but it should output it the way i intended it, otherwise the health/inventory tracking wont work.
