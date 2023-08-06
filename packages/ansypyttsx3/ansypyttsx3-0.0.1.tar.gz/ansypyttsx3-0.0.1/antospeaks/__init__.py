import pyttsx3


engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
volume = engine.getProperty('volume')
engine.setProperty('voice', voices[0].id)   
engine.setProperty('volume', volume+10)

def speak (audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    

