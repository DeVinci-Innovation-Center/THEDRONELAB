from pynput import keyboard
import time

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
            land=True
        if(key == keyboard.Key.right):
            print("RIIGHT")

        if(key == keyboard.Key.left):
            print("LEFT")

        if(key == keyboard.Key.up):
            print("UP")

        if(key == keyboard.Key.down):
            print("DOWN")


listener = keyboard.Listener(
    on_press=on_press)
listener.start()

start=time.time()
time.sleep(1)
while(time.time()-start<20):
    time.sleep(1)

        
