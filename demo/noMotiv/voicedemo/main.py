# import speech_recognition as sr
# import logging
# import time

# import cflib.crtp
# from cflib.crazyflie import Crazyflie
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.utils import uri_helper

# from cflib.crazyflie.log import LogConfig
# from cflib.crazyflie.syncLogger import SyncLogger
# from cflib.positioning.motion_commander import MotionCommander
# logging.basicConfig(level=logging.ERROR)

# global takeOff
# takeOff = False

# def speech():   
#     global takeOff
#     with sr.Microphone() as source:
#         print("Speak Anything :")
#         audio = r.listen(source,timeout=3)   
#         text = r.recognize_google(audio)
#         print("You said : {}".format(text))
#         if (format(text)=="take off"):
#             takeOff = True


# URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E703')
# r = sr.Recognizer()

# #if __name__ == '_main_':


    
#     with sr.Microphone() as source:
#         print("Speak Anything :")
#         audio = r.listen(source,timeout=3)   
#         text = r.recognize_google(audio)
#         print("You said : {}".format(text))
#         if (format(text)=="take off"):
#             takeOff = True
        
#         cflib.crtp.init_drivers() 
#         with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
#             # We take off when the commander is created
#             while(takeOff):
#                 with MotionCommander(scf) as mc:
#                     start=time.time()
#                     while(time.time()-start<5):
#                         time.sleep(1)
#                         print(time.time()-start)
#                     mc.stop()
#                     takeOff=False

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
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie import Commander
logging.basicConfig(level=logging.ERROR)

global takeOff
takeOff = False
vitesse = 0.1
global droite
droite = False
global gauche
gauche = False
global avant
avant = False
global arriere
arriere = False
global land
land=False
global cercle
cercle=False
global monter
monter=False
global descendre
descendre=False
global danse
danse=False

def speech():   
    global takeOff
    global droite
    global gauche
    global avant
    global arriere
    global land
    global cercle
    global monter
    global descendre
    global danse
    with sr.Microphone() as source:
        try:
            print("Speak Anything :")
            audio = r.listen(source, phrase_time_limit=2)   
            text = r.recognize_google(audio, language="fr-FR")
            print("You said : {}".format(text))
            if (format(text)=="d??collage"):
                takeOff = True
            if (format(text)=="droite"):
                droite = True
            if (format(text)=="gauche"):
                gauche = True
            if (format(text)=="avant"):
                avant = True
            if (format(text)=="arri??re"):
                arriere = True
            if (format(text)=="atterrissage"):
                land = True
            if (format(text)=="cercle"):
                cercle = True
            if (format(text)=="monter"):
                monter = True                
            if (format(text)=="descendre"):
                descendre = True   
            if (format(text)=="danse"):
                danse = True                              
        except: 
            print("fail to listen")


URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E701')
# URI2 = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E705')

r = sr.Recognizer()

with sr.Microphone() as source:
    cflib.crtp.init_drivers() 
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            with SyncCrazyflie(URI2, cf=Crazyflie(rw_cache='./cache')) as sf:       
                start=time.time()
                while(time.time()-start<60):
                    speech()
                    if(takeOff):
                        takeOff=False
                        with MotionCommander(scf,default_height=0.3) as mc:
                            with MotionCommander(sf,default_height=0.3) as mcf:

                                while(time.time()-start<60):
                                    time.sleep(1)
                                    print(time.time()-start)
                                    speech()
                                    if(droite):
                                        mc.right(distance_m=0.4,velocity=0.2)
                                        mcf.right(distance_m=0.4,velocity=0.2)
                                        droite = False
                                    if(gauche):
                                        mc.left(distance_m=0.4,velocity=0.2)
                                        gauche = False
                                    if(avant):
                                        mc.forward(distance_m=0.4,velocity=0.2)
                                        avant = False
                                    if(arriere):
                                        mc.back(distance_m=0.4,velocity=0.2)
                                        arriere = False
                                    if(land):
                                        mc.land(velocity=0.3)
                                        land=False
                                    if(takeOff):
                                        mc.take_off(velocity=0.2)
                                        takeOff=False
                                    if(cercle):
                                        mc.circle_left(radius_m=0.4,velocity=0.4,angle_degrees=360)
                                        cercle=False
                                    if(monter):
                                        mc.up(distance_m=0.3,velocity=0.2)
                                        monter=False
                                    if(descendre):
                                        mc.down(distance_m=0.3,velocity=0.2)
                                        descendre=False
                                    if(danse):
                                        mc.left(0.3,velocity=0.6)
                                        mc.forward(0.3,velocity=0.6)
                                        mc.right(0.3,velocity=0.6)
                                        mc.back(0.3,velocity=0.6)
                                        mc.up(0.3,velocity=0.6)
                                        mc.right(0.3,velocity=0.6)
                                        danse =False
                                        
                                        

                                mc.stop()
