from ssl import ALERT_DESCRIPTION_INTERNAL_ERROR
from sys import dont_write_bytecode
from cflib import crazyflie
import speech_recognition as sr
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie import Commander
logging.basicConfig(level=logging.ERROR)


takeOff = False
vitesse = 0.1


def speech():   
    
    with sr.Microphone() as source:
        try:
            print("Speak")
            audio = r.listen(source, phrase_time_limit=3)   
            text = r.recognize_google(audio, language="fr-FR")
            print("You said : {}".format(text))
            return text
        except: 
            print("fail to listen")
            return ""

def reco():
    global takeOff
    global words
    

    if("drone" in words):
        print('Trigger word found')
        words+=" end"
        beginning = words.find("drone")
        words = words[beginning::]
        print(words)
        arr = words.split(" ")
        if(arr[1]):
            text=arr[1]
            print(text)
            if (text=="décollage"& takeOff==False):
                takeOff = True            
            if (format(text)=="droite"):
                mc.right(distance_m=0.4,velocity=0.2)
            if (format(text)=="gauche"):
                mc.left(distance_m=0.4,velocity=0.2)
            if (format(text)=="avant"):
                mc.forward(distance_m=0.4,velocity=0.2)
            if (format(text)=="arrière"):
                mc.back(distance_m=0.4,velocity=0.2)
            if ("atteri" in text):
                mc.land(velocity=0.3)
            if (format(text)=="monter"):
                mc.up(distance_m=0.4,velocity=0.2)
            if (format(text)=="descendre"):
                mc.down(distance_m=0.4,velocity=0.2)
            if (format(text)=="danse"): 
                danse = True                              
            if (format(text)=="maison"):
                mc.go_to(0,0,z=0.3,velocity=0.2)
                time.sleep(1)
                mc.land(velocity=0.2)
                maison = True
            words=""            



URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E701')

r = sr.Recognizer()

with sr.Microphone() as source:
    cflib.crtp.init_drivers() 
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf: 
        start=time.time()
        words=""
        while(time.time()-start<320):
            words+=" "+speech()
            reco()
            if(takeOff):
                print("gogo")
                takeOff=False
                with PositionHlCommander(scf,default_height=0.7) as mc:
                    while(time.time()-start<280):
                        words+=" "+speech()
                        reco()
                        # if(droite):
                        #     mc.right(distance_m=0.4,velocity=0.2)
                        #     droite = False
                        # if(gauche):
                        #     mc.left(distance_m=0.4,velocity=0.2)
                        #     gauche = False
                        # if(avant):
                        #     mc.forward(distance_m=0.4,velocity=0.2)
                        #     avant = False
                        # if(arriere):
                        #     mc.back(distance_m=0.4,velocity=0.2)
                        #     arrieif(droite):
                        #     mc.right(distance_m=0.4,velocity=0.2)
                        #     droite = False
                        # if(gauche):
                        #     mc.left(distance_m=0.4,velocity=0.2)
                        #     gauche = False
                        # if(avant):
                        #     mc.forward(distance_m=0.4,velocity=0.2)
                        #     avant = False
                        # if(arriere):
                        #     mc.back(distance_m=0.4,velocity=0.2)
                        #     arriere = False
                        # if(land):
                        #     #mc.land(velocity=0.3)
                        #     land=False
                        # if(takeOff):
                        #     mc.take_off(height=0.7,velocity=0.5)
                        #     takeOff=False
                        # if(cercle):
                        #     mc.circle_left(radius_m=0.4,velocity=0.4,angle_degrees=360)
                        #     cercle=False
                        # if(monter):
                        #     mc.up(distance_m=0.3,velocity=0.2)
                        #     monter=False
                        # if(descendre):
                        #     mc.down(distance_m=0.3,velocity=0.2)
                        #     descendre=False
                        # if(danse):
                        #     mc.left(0.3,velocity=0.6)
                        #     mc.forward(0.3,velocity=0.6)
                        #     mc.right(0.3,velocity=0.6)
                        #     mc.back(0.3,velocity=0.6)
                        #     mc.up(0.3,velocity=0.6)
                        #     mc.right(0.3,velocity=0.6)
                        #     danse =False
                        # if(maison):
                        #     mc.go_to(0,0,z=0.3,velocity=0.2)
                        #     time.sleep(1)
                        #     mc.land(velocity=0.2)
                        #     maison=False
                        re = False
                        # if(land):
                        #     #mc.land(velocity=0.3)
                        #     land=False
                        # if(takeOff):
                        #     mc.take_off(height=0.7,velocity=0.5)
                        #     takeOff=False
                        # if(cercle):
                        #     mc.circle_left(radius_m=0.4,velocity=0.4,angle_degrees=360)
                        #     cercle=False
                        # if(monter):
                        #     mc.up(distance_m=0.3,velocity=0.2)
                        #     monter=False
                        # if(descendre):
                        #     mc.down(distance_m=0.3,velocity=0.2)
                        #     descendre=False
                        # if(danse):
                        #     mc.left(0.3,velocity=0.6)
                        #     mc.forward(0.3,velocity=0.6)
                        #     mc.right(0.3,velocity=0.6)
                        #     mc.back(0.3,velocity=0.6)
                        #     mc.up(0.3,velocity=0.6)
                        #     mc.right(0.3,velocity=0.6)
                        #     danse =False
                        # if(maison):
                        #     mc.go_to(0,0,z=0.3,velocity=0.2)
                        #     time.sleep(1)
                        #     mc.land(velocity=0.2)
                        #     maison=False
                        
                    
                    mc.land()
                
