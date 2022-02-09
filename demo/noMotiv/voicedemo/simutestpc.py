from posixpath import realpath
from ssl import ALERT_DESCRIPTION_INTERNAL_ERROR
from sys import dont_write_bytecode
from cflib import crazyflie
import speech_recognition as sr
import logging
import time
from pycrazyswarm import *
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
import numpy as np
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie import Commander
import sys
logging.basicConfig(level=logging.ERROR)


takeOff = False
vitesse = 0.1

droite = False

gauche = False
avant = False
arriere = False

land=False

cercle=False

monter=False

descendre=False

danse=False
maison = False

def speech():   
    
    with sr.Microphone() as source:
        try:
            print("Speak")
            audio = r.listen(source, phrase_time_limit=2)   
            text = r.recognize_google(audio, language="fr-FR")
            print("You said : {}".format(text))
            return text
        except: 
            print("fail to listen")
            return ""

def reco():
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
    global maison
    global words
    if("drone " in words):
        print("go")
        beginning = words.find("drone")
        words = words[beginning::]
        arr = words.split(" ")
        if(arr[1]):
            text=arr[1]
            print(text)
            if (text=="décollage"):
                takeOff = True
                print("go2")
            if (format(text)=="droite"):
                droite = True
            if (format(text)=="gauche"):
                gauche = True
            if (format(text)=="avant"):
                avant = True
            if (format(text)=="arrière"):
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
            if (format(text)=="maison"):
                maison = True
            words=""            



URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E701')

r = sr.Recognizer()

with sr.Microphone() as source:
    print(sys.argv)
    cs = Crazyswarm("/home/anne/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml", args=sys.argv)
    TimeHelper = cs.timeHelper
    TimeHelper.sleep(0.1)
    for i in cs.allcfs.crazyflies:
        if i.id == 1:
            cf = i
    start=time.time()
    words=""
    while(time.time()-start<320):
        words+=" "+speech()
        reco()

        if(takeOff):
            print("gogo")
            takeOff=False
            # cf.takeoff(1,2)
            cf.goTo(np.array([0,0,1]),0,0,2,True)
            while(time.time()-start<280):
                #print(time.time()-start)
                TimeHelper.sleep(0.1)
                words+=" "+speech()
                reco()
                if(droite):
                    cf.goTo(np.array([0.4,0,0]),0,0.2, True)
                    droite = False
                if(gauche):
                    cf.goTo(np.array([-0.4,0,0]),0,0.2, True)
                    # mc.left(distance_m=0.4,velocity=0.2)
                    gauche = False
                if(avant):
                    cf.goTo(np.array([0,0.4,0]),0,0.2, True)
                    # mc.forward(distance_m=0.4,velocity=0.2)
                    avant = False
                if(arriere):
                    cf.goTo(np.array([0,-0.4,0]),0,0.2, True)
                    # mc.back(distance_m=0.4,velocity=0.2)
                    arriere = False
                if(land):
                    # mc.land(velocity=0.3)
                    cf.land()
                    land=False
                if(takeOff):
                    cf.takeoff(1,2)
                    takeOff=False
                if(cercle):
                    # mc.circle_left(radius_m=0.4,velocity=0.4,angle_degrees=360)
                    cercle=False
                if(monter):
                    # mc.up(distance_m=0.3,velocity=0.2)
                    monter=False
                if(descendre):
                    # mc.down(distance_m=0.3,velocity=0.2)
                    descendre=False
                if(danse):
                    # mc.left(0.3,velocity=0.6)
                    # mc.forward(0.3,velocity=0.6)
                    # mc.right(0.3,velocity=0.6)
                    # mc.back(0.3,velocity=0.6)
                    # mc.up(0.3,velocity=0.6)
                    # mc.right(0.3,velocity=0.6)
                    danse =False
                if(maison):
                    # mc.go_to(0,0,z=0.3,velocity=0.2)
                    time.sleep(1)
                    # mc.land(velocity=0.2)
                    maison=False
                
                
                    # mc.land()
                    cf.stop()
            
