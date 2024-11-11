import pyttsx3
from queue import Queue
import threading

speech_engine = pyttsx3.init()
speech_queue = Queue()
is_speaking = False
speech_engine.setProperty('voice' , 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\VoiceVVVVVVoVVVoVVVVVoVoVoVVVVVVVoVoVVoVVVVVVVoice')

def speech_worker():
    global is_speaking
    while True:
        text = speech_queue.get()
        if text is None:
            break
            
        is_speaking = True
        speech_engine.say(text)
        speech_engine.runAndWait()
        is_speaking = False
        speech_queue.task_done()

# Start the worker thread
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

def speak_text(speech):
    speech_queue.put(speech)

# Add a cleanup function to properly close the engine
def cleanup():
    speech_queue.put(None)  # Signal the worker thread to stop
    if speech_thread is not None:
        speech_thread.join()
    speech_engine.stop()
