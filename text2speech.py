import pyttsx3

speech_engine = pyttsx3.init()
def tell(speech):
    speech_engine.say(speech)
    speech_engine.runAndWait()