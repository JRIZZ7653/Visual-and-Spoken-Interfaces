import speech_recognition
import pyttsx3
import customtkinter
from googletrans import Translator, constants
from pprint import pprint

translator = Translator()

root = customtkinter.CTk()
root.geometry("500x680")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

recognizer = speech_recognition.Recognizer()

engine = pyttsx3.init()

chosenLanguage = ""

translation = ""

def findSpeech():

	with speech_recognition.Microphone() as mic:
		recognizer.adjust_for_ambient_noise(mic, duration=0.2)
		audio = recognizer.listen(mic)

		text = recognizer.recognize_google(audio)
		text = text.lower()
		#print(text)
			
		# Translate the speech
		global translation
		translation = translator.translate(text, dest=chosenLanguage)
		#print the translation

		label3.configure(text =(f"{translation.text}" ))  # display that value on a label in tkinter
		label3.update_idletasks()

		#print(translation.text)

def saySpeech():
	global translation
	engine.say(translation.text)
	engine.runAndWait()

	
def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

    global chosenLanguage
    chosenLanguage = choice
		

label = customtkinter.CTkLabel(master=root, text="RealTime SubTitles", font=("Roboto", 24))
label.place(x=200, y=10)

label2 = customtkinter.CTkLabel(master=root, text="By Jake Risley", font=("Roboto", 8))
label2.place(x=200, y=33)

frame1 = customtkinter.CTkFrame(master=root, width=480, height=600, fg_color="grey")
frame1.place(x=10, y=70)

label3 = customtkinter.CTkLabel(master=frame1, text="", font=("Roboto", 25), wraplength=460)
label3.place(x=10, y=40)

button1 = customtkinter.CTkButton(frame1, text="Start Translator", width=125, height=105, command=findSpeech)
button1.place(x=10, y=470)

button2 = customtkinter.CTkButton(frame1, text="Say", width=125, height=105, command=saySpeech)
button2.place(x=140, y=470)

optionmenu = customtkinter.CTkOptionMenu(frame1, values=["en", "fr", "es", "ja"],
                                         command=optionmenu_callback)
optionmenu.set("Select Language")
optionmenu.place(x=300, y=500)

root.mainloop()