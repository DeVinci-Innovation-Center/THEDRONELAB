from os import W_OK
import speech_recognition as sr
import time

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
        if("drone" in words):
            print("COMMAND detected")
            beginning = words.find("drone")
            words = words[beginning::]
            wordarr = words.split(" ")
            print(len(wordarr))
            print(words)
            words=""
