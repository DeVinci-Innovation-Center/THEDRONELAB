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
URI = uri_helper.uri_from_env(default='radio://0/27/2M/E7E7E7E701')
vector=np.array([0.0,0.0,0.0])

def on_press(key):
    global Land
    global vector
    global mode
    global rest
    travel = 0.3  
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        if(key.char=='h'): #home
            print("HOME MODE")
            Land=True
            mode=3

        if(key.char=='m'): #manual
            print("MANUAL MODE")
            pc.go_to(0,0,0.4)
            mode=2
            #pc.start_linear_motion(vector[0],vector[1],vector[2])
        if(key.char=='a'): #auto
            print("AUTO MODE")
            pc.go_to(0,0,0.4)
            mode=1
        if(key.char=='r'): #home
            print("RESET")
            rest=True
            mode=3
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
            if(key == keyboard.Key.shift):
                print("TOP")
                vector[1]=0
                vector[2]=travel
            if(key == keyboard.Key.ctrl):
                print("BELOW")
                vector[0]=0
                vector[1]=0
                vector[2]=-travel

        # vector=np.array([0.0,0.0,0.0])
        
if __name__ == '__main__':
    global mode
    global rest
    rest=False
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
            global list
            list=[[0,0,0.4],[0.3,0,0],[0,0.3,0],[-0.3,0,0],[0,-0.3,0],[0,0,-0.4],[0.3,0,0],[0,0.3,0],[-0.3,0,0],[0,-0.3,0]]
            i=0
            while(time.time()-start<20):
                
                if(mode==1 and i<=9):
                    pc.move_distance(list[i][0],list[i][1],list[i][2])
                    i=i+1
                    print("I:"+str(i))
                    rest=False
                if(rest and i>9):
                    print("I:"+str(i))
                    i=0


                if(mode==2):
                    pc.move_distance(vector[0],vector[1],vector[2])

                if(Land):
                    pc.go_to(0,0,0.3)
                    pc.land
                
                if(int(time.time()-start)!=a):
                    print(time.time()-start) 
                    a=int(time.time()-start  )
                    print(str(time.time()-start)+"mode -"+ str(mode) +"-") 