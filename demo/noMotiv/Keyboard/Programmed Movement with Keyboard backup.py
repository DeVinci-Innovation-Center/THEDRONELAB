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
URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E705')
vector=np.array([0.0,0.0,0.0])

def on_press(key):
    global Land
    global vector
    travel = 0.3  
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        if(mode==2):

            if(key.char=='t'):
                print("TOP")
                vector[0]= 0
                vector[1]=0
                vector[2]=travel
            if(key.char=='g'):
                print("BELOW")
                vector[0]=0   
                vector[1]=0
                vector[2]=-travel
        if(key.char=='h'): #home
            print("HOME MODE")
            Land=True
            mode=3

        if(key.char=='m'): #manual
            print("MANUAL MODE")
            mode=2
            #pc.start_linear_motion(vector[0],vector[1],vector[2])
        if(key.char=='a'): #auto
            print("AUTO MODE")
            mode=1
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if(mode==2):
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
                vector[1]= -travel
                vector[2]=0

        # vector=np.array([0.0,0.0,0.0])
        
if __name__ == '__main__':
    global mode
    mode =1
    
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
        with PositionHlCommander(scf) as pc:
            print("TAKE OFF")
            start=time.time()
            time.sleep(1)
            list=[[0,0,0.4],[0.3,0,0],[0,0.3,0],[-0.3,0,0],[0,-0.3,0],[0,0,-0.4],[0.3,0,0],[0,0.3,0],[-0.3,0,0],[0,-0.3,0]]
            i=0
            while(time.time()-start<15):
                if(mode==1&i<9):
                    pc.move_distance(list[i][0],list[i][1],list[i][2])
                    print(list[i])
                    i=i+1

                if(mode==2):
                    pc.move_distance(vector[0],vector[1],vector[2])

                if(Land):
                    pc.go_to(0,0,0.3)
                    pc.land
                
                if(int(time.time()-start)!=a):
                    print(time.time()-start) 
                    a=int(time.time()-start  ) 
                if(Land):
                    break





















if __name__ == '__main__':
    

    listener = keyboard.Listener(
    on_press=on_press)
    listener.start()

    start=time.time()
    time.sleep(1)
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
            pc.circle_right(0.4, velocity=0.5, angle_degrees=180)
            time.sleep(1)
            pc.land()
            while(time.time()-start<20):  
                time.sleep(1)
    
    
                

