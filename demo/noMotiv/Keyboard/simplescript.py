import logging
import time
import numpy as np

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.motion_commander import MotionCommander
logging.basicConfig(level=logging.ERROR)

from pynput import keyboard

land =False
URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E704')
vector=np.array([0,0,0])
def on_press(key):
    global land
    global vector
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))   
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if(key == keyboard.Key.space):
            print("LANDING  ")      
            land=True
        if(key == keyboard.Key.right):
            print("RIIGHT")
            vector[0]+=0.1
        if(key == keyboard.Key.left):
            print("RIIGHT")
            vector[0]-=0.1
        if(key == keyboard.Key.up):
            print("RIIGHT")
            vector[1]+=0.1
        if(key == keyboard.Key.down):
            print("RIIGHT")
            vector[1]-=0.1
        mc.move_distance(*vector)
        vector=[0,0,0]



  

if __name__ == '__main__':
    
    cflib.crtp.init_drivers() 

    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        
        with MotionCommander(scf) as mc:
            start=time.time()
            while(time.time()-start<5):
                time.sleep(1)
                if(land):
                    break

                print(time.time()-start)
            mc.stop()


        

