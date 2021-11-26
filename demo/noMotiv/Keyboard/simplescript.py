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

Land=False
URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E704')
vector=np.array([0.0,0.0,0.0])

def on_press(key):
    global land
    global vector
    travel = 0.3
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))   
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if(key == keyboard.Key.space):
            print("LANDING  ")          
            mc.land
        if(key == keyboard.Key.right):
            print("RIIGHT")
            vector[0]=travel
        if(key == keyboard.Key.left):
            print("LEFT")
            vector[0]=-travel
        if(key == keyboard.Key.up):
            print("UP")
            vector[1]=travel
        if(key == keyboard.Key.down):  
            print("DOWN")
            vector[1]=-travel
        
        mc.start_linear_motion(*vector)
        # vector=np.array([0.0,0.0,0.0])
        
        
        



  

if __name__ == '__main__':
    
    cflib.crtp.init_drivers() 

    listener = keyboard.Listener(
        on_press=on_press)  
    listener.start()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        print("TAKE OFF")
        a=0
        with MotionCommander(scf) as mc:
            start=time.time()
            time.sleep(1)
            while(time.time()-start<10):

                if(int(time.time()-start)!=a):
                    print(time.time()-start) 
                    a=int(time.time()-start  ) 
                if(Land):
                    break


                