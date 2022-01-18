#from os import W_OK
import speech_recognition as sr
import time
from playsound import playsound
def speech(source):   
    try :
        # print("Speak Anything :")
        audio = r.listen(source, phrase_time_limit=4)   
        text = r.recognize_google(audio, language="fr-FR")
        # print("You said : {}".format(text))
        return text
    except :
        # print("FAIL")
        return ""

def token(x):
    return {
        "alpha": 1,
        "espilon": 2,
    }.get(x, 0)

def command(x):
    return {
        "décollage": 1,
        "droite": 2,
    }.get(x, 0)

r = sr.Recognizer()

with sr.Microphone() as source:
    # try :
    #     print("Speak Anything :")
    #     audio = r.listen(source, phrase_time_limit=4)   
    #     text = r.recognize_google(audio)
    #     print("You said : {}".format(text))
    # except :
    #     print("FAIL")
    

    start=time.time()
    words=""
    while(time.time()-start<60):
        #time.sleep(1)
        print(time.time()-start)
        print(words)
        words+=" "+speech(source)
        if("drone " in words):
            print("COMMAND detected")
            beginning = words.find("drone")
            words = words[beginning::]
            wordarr = words.split(" ")
            if(wordarr[1]):
                droneNumber = token(wordarr[1])
                print("token :"+wordarr[1])
                print("new token :"+droneNumber)
                if (droneNumber): 
                    if(command(wordarr[2])):
                        print("good")
                    else: break
                else: break
                print(words)
                words=""
        if("explosion" in words):
            words=words.replace("explosion","") 
            playsound('/home/anne/Downloads/bruit-dexplosion.mp3')
   


  