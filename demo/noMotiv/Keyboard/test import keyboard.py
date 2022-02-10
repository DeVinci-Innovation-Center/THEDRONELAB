from pynput import keyboard
import time

def on_press(key):
    global land
    global vector
    travel = 0.3
    try:
        print('alphanumeric key -{0}- pressed'.format(
            key.char))   
        if(key.char=='t'):
            print("TOP")

        if(key.char=='g'):
            print("DOWN")

    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if(key == keyboard.Key.space):
            print("LANDING  ")      
            land=True
        if(key == keyboard.Key.right):
            print("RIIGHT")
            time.sleep(1)

        if(key == keyboard.Key.left):
            print("LEFT")
            time.sleep(1)

        if(key == keyboard.Key.up):
            print("UP")

        if(key == keyboard.Key.down):
            print("DOWN")
        if(key == keyboard.Key.ctrl_r):
            print("right ctrl")
        if(key== keyboard.Key.ctrl_l):
            print("Left ctrl")
        if(key== keyboard.Key.alt_l):
            print("Left alt")


listener = keyboard.Listener(
    on_press=on_press)
listener.start()

start=time.time()
time.sleep(1)
while(time.time()-start<20):
    time.sleep(1)

        
