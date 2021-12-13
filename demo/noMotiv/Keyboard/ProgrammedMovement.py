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
from cflib.positioning.position_hl_commander import PositionHlCommander
logging.basicConfig(level=logging.ERROR)

from pynput import keyboard
Land=False

def Startdemo():
    URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E705')
    vector=np.array([0.0,0.0,0.0])
    cflib.crtp.init_drivers() 
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        
        a=0 
        time.sleep(1)
        print("COMMING") 
        with PositionHlCommander(scf) as pc:
            print("STARTING")
            pc.forward(0.3)
            pc.left(0.3)
            pc.back(0.3)
            pc.right(0.3)
            pc.up(0.3)
            pc.forward(0.3)
            pc.left(0.3)
            pc.back(0.3)
            pc.right(0.3)
            #pc.circle_right(0.4, velocity=0.5, angle_degrees=180) 
            time.sleep(1)
            pc.land()
            
            # pc.go_to(0.0, 0.0, 1.0)
            

 
def on_press(key):
    global Land
    global vector
    travel = 0.2  
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))   
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if(key == keyboard.Key.space):
            print("Demo start ")  
            Startdemo()        
        
if __name__ == '__main__':
    

    listener = keyboard.Listener(
    on_press=on_press)
listener.start()
start=time.time()
time.sleep(1)
while(time.time()-start<20):  
    time.sleep(1)
    
    
          

