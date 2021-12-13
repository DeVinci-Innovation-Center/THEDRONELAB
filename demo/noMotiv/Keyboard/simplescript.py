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
URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E705')
vector=np.array([0.0,0.0,0.0])

def on_press(key):
    global Land
    global vector
    travel = 0.3  
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))  
        if(key.char=='t'):
            print("TOP")
            vector[0]=0
            vector[1]=0
            vector[2]=travel
        if(key.char=='g'):
            print("BELOW")
            vector[0]=0
            vector[1]=0
            vector[2]=-travel
    except AttributeError :
        print('special key {0} pressed'.format(
            key))
        if(key == keyboard.Key.space):
            mc.move_distance(0.0,0.0,-0.3)
            mc.land
            Land=True
            print("LANDING  ")          
        if(key == keyboard.Key.right):
            print("RIIGHT")
            vector[0]=travel
            vector[1]=0
            vector[2]=0
        if(key == keyboard.Key.left):
            print("LEFT")
            vector[0]=-travel
            vector[1]=0
            vector[2]=0
        if(key == keyboard.Key.up):
            print("UP")
            vector[0]=0
            vector[1]=travel
            vector[2]=0
        if(key == keyboard.Key.down):  
            print("DOWN")
            vector[0]=0
            vector[1]=-travel
            vector[2]=0

        mc.start_linear_motion(vector[0],vector[1],vector[2])
        # vector=np.array([0.0,0.0,0.0])
        
if __name__ == '__main__':
    
    cflib.crtp.init_drivers() 

    listener = keyboard.Listener(
        on_press=on_press)  
    listener.start()
    #global is_deck_attached
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        
        a=0
          # scf.cf.param.add_update_callback(group="deck", name="bcFlow2",
        #                         cb=param_deck_flow)
        time.sleep(1)
        
        # if is_deck_attached:
        with MotionCommander(scf) as mc:
            
            print("TAKE OFF")
            start=time.time()
            time.sleep(1)
            mc.move_distance(0.0,0.0,0.3)
            while(time.time()-start<30):
                if(int(time.time()-start)!=a):
                    print(time.time()-start) 
                    a=int(time.time()-start  ) 
                    

                if(Land):
                    break




















