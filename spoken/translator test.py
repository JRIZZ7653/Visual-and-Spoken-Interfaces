from googletrans import Translator, constants
from pprint import pprint

translator = Translator()


inputText = input("Text to translate >> ")

translation = translator.translate(inputText, dest="fr")
print(f"{translation.text} ({translation.dest})")