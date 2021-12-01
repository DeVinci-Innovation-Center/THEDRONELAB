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
logging.basicConfig(level=logging.ERROR)

def speech():   
    global takeOff
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source,timeout=3)   
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
        if (format(text)=="take off"):
            takeOff = True

if __name__ == '_main_':

    global vol
    vol = False
URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E703')
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak Anything :")
    audio = r.listen(source,timeout=3)   
    text = r.recognize_google(audio)
    print("You said : {}".format(text))
    if (format(text)=="take off"):
        vol = True
    
    cflib.crtp.init_drivers() 
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        if(vol==True):
            with MotionCommander(scf) as mc:
                start=time.time()
                while(time.time()-start<5):
                    time.sleep(1)
                    print(time.time()-start)
                    speech()
                mc.stop()