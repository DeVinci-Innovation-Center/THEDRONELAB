# Let's do a local graph of an existing circle.

# Then find how to update position in realtime on same graph.

# Then find how to trace position accurately.

# x and y given as array_like objects
import dash
from dash import dcc
#import dash_core_components as dcc
from dash import html
#import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import queue
import logging
import time
import threading
import multiprocessing
import dvbcdr
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
import keyboard
from queue import Empty
from queue import Queue
from threading import Thread
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="scatter-plot"),

    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
    ),
    dcc.Store(id='intermediate-value')
])

class _SetPointThread(Thread):
    TERMINATE_EVENT = 'terminate'
    UPDATE_PERIOD = 0.2
    ABS_Z_INDEX = 3

    def __init__(self, cf, update_period=UPDATE_PERIOD):
        Thread.__init__(self)
        self.update_period = update_period

        self._queue = Queue()
        self._cf = cf

        self._hover_setpoint = [0.0, 0.0, 0.0, 0.0]

        self._z_base = 0.0
        self._z_velocity = 0.0
        self._z_base_time = 0.0

    def stop(self):
        """
        Stop the thread and wait for it to terminate
        :return:
        """
        self._queue.put(self.TERMINATE_EVENT)
        self.join()

    def set_vel_setpoint(self, velocity_x, velocity_y, velocity_z, rate_yaw):
        """Set the velocity setpoint to use for the future motion"""
        self._queue.put((velocity_x, velocity_y, velocity_z, rate_yaw))

    def get_height(self):
        """
        Get the current height of the Crazyflie.
        :return: The height (meters)
        """
        return self._hover_setpoint[self.ABS_Z_INDEX]

    def run(self):
        while True:
            try:
                event = self._queue.get(block=True, timeout=self.update_period)
                if event == self.TERMINATE_EVENT:
                    return

                self._new_setpoint(*event)
            except Empty:
                pass

            self._update_z_in_setpoint()
            self._cf.commander.send_hover_setpoint(*self._hover_setpoint)

    def _new_setpoint(self, velocity_x, velocity_y, velocity_z, rate_yaw):
        self._z_base = self._current_z()
        self._z_velocity = velocity_z
        self._z_base_time = time.time()

        self._hover_setpoint = [velocity_x, velocity_y, rate_yaw, self._z_base]

    def _update_z_in_setpoint(self):
        self._hover_setpoint[self.ABS_Z_INDEX] = self._current_z()

    def _current_z(self):
        now = time.time()
        return self._z_base + self._z_velocity * (now - self._z_base_time)


def simple_log(scf, logconf):
    with SyncLogger(scf, lg_stab) as logger:

        for log_entry in logger:

            timestamp = log_entry[0]
            data = log_entry[1]
            logconf_name = log_entry[2]

            print('[%d][%s]: %s' % (timestamp, logconf_name, data))

            #break

def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(DEFAULT_TRANSLATION)
        time.sleep(1)
        mc.back(DEFAULT_TRANSLATION)
        time.sleep(1)

def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(3)
        mc.stop()

#mc.circle_right(0.5, velocity=0.5, angle_degrees=180)
def move_circle_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        mc.circle_right(0.3, velocity=0.3)
        time.sleep(3)
        mc.stop()
#move_distance(self, distance_x_m, distance_y_m, distance_z_m,
#                      velocity=VELOCITY)
def move_translation(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        mc.move_distance(distance_x_m=DEFAULT_TRANSLATION, distance_y_m=DEFAULT_TRANSLATION, distance_z_m=DEFAULT_TRANSLATION,
                      velocity=0.3)
        time.sleep(1)
        mc.stop()

def move_square(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        for vector3 in spiral_points:
            mc.move_distance(distance_x_m=vector3[0], distance_y_m=vector3[1], distance_z_m=vector3[2],
                        velocity=0.5)
            #time.sleep(1)
        mc.land()


def move_Q(scf):
    global Q
    start = time.time()
    move = -0.001
    movez = 0.0
    now = time.time()
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        while time.time() - start < 20:
            intercom.run_callbacks()
            print(Q.empty())
            if not Q.empty():
                action = Q.get()
                print("----------ACTION : ", action)
                if action in "LEFTTHUMBUP":
                    move = 0.005 # initial value : 0.01
                else:
                    move = -0.005 # initial value : 0.01
                    
                
            mc.move_distance(distance_x_m=move, distance_y_m=0, distance_z_m=0, velocity=0.3)
            # if time.time() - now > 3:
            #     now = time.time()
            #     move *= -1
        mc.land()

def move_up_and_release(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        mc.move_distance(distance_x_m=0.0, distance_y_m=0.0, distance_z_m=1.5,
                      velocity=0.3)
        time.sleep(2)
        mc.move_distance(distance_x_m=0.0, distance_y_m=0.0, distance_z_m=-1.0,
                      velocity=100.0)
        time.sleep(2)
        print('Currently drops automatically.')
        # while True:  # making a loop
        #     try:  # used try so if user pressed other than the given key error will not be shown
        #         if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        #             print('You Pressed A Key!')
        #             break
        #     except:
        #         time.sleep(0.01)
        #         pass

        # while (not keyboard.is_pressed('q')):  # making a loop
        #     time.sleep(0.01)

        mc._thread.stop()
        mc._thread = None
        mc._cf.commander.send_stop_setpoint()
        #mc.stop()

def demo_rotation_speeds(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        mc.move_distance(distance_x_m=0.0, distance_y_m=0.0, distance_z_m=0.08,
                      velocity=0.3)
        time.sleep(4)
        print('Currently rotates automatically.')
        #mc.turn_left(360, rate = 360.0 / 3 )
        #mc.turn_left(360, rate = 360.0 / 2 )
        #mc.turn_left(360, rate = 360.0 / 1 )
        mc.turn_left(720, rate = 360.0 * 1 )
        mc.stop()

def FF_recover(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:

        #mc.land()
        #time.sleep(2)
        print('Currently turns off and on again.')


        mc.move_distance(distance_x_m=0.0, distance_y_m=0.0, distance_z_m=1.8,
                      velocity=0.3)
        
        # mc.move_distance(distance_x_m=0.0, distance_y_m=0.0, distance_z_m=-3.0,
        #               velocity=1.0)       

        # print('TURN OFF.')
        # mc._thread.stop() 
        # mc._thread = None
        # mc._cf.commander.send_stop_setpoint()
        # mc._is_flying = False

        # # height = 1.0
        # # while(height>0.3):
        # #     #height = height - 0.01
        # #     print('sup')
        # #     height = 0.3
        #     #pass
        # time.sleep(0.32)
        
        # #mc.stop()
        # print('TURN ON.')
        # mc._is_flying = True
        # #mc._reset_position_estimator()
        # mc._thread = _SetPointThread(mc._cf)
        # #mc._thread._z_base = 1.0
        # mc._thread.start()

        # mc.move_distance(distance_x_m=0.0, distance_y_m=0.0, distance_z_m=-0.2,
        #               velocity=0.1)
        # #mc.take_off()
        # #height = mc.default_height
    
        # mc.land()        

def param_deck_flow(name, value_str):
    value = int(value_str)
    print(value)
    global is_deck_attached
    if value:
        is_deck_attached = True
        print('Deck is attached!')
    else:
        is_deck_attached = False
        print('Deck is NOT attached!')


class Log2App:

    def __init__(self, filename='dynamic_graphing.txt'):
        self.filename=filename
        self.x=0.0
        self.y=0.0
        self.z=0.0
        with open(self.filename, 'w') as f:
            f.write('init done')

    def log_pos_callback(self, timestamp, data, logconf):
        self.x=data['stateEstimate.x']
        self.y=data['stateEstimate.y']
        #self.z=data['stateEstimate.z'] ###########
        with open(self.filename, 'w') as f:
            f.write(str(self.x)+' '+str(self.y))
            f.close()
        #print( "log", self.x, self.y, timestamp)
        #return x, y
# PROBLEM IS HERE.
def global_to_app(self):
    new_data=[self.x, self.y]
    return new_data
    
@app.callback(Output('intermediate-value', 'data'), 
            Input('interval-component', 'n_intervals') )
def clean_data(n):
    data_string = open('dynamic_graphing.txt', 'r').read() 
    #print("app", self.global_to_app())
    data = data_string.split(' ')

    array=[]
    for each in data:
        value = float(each)
        array.append(value)
    print(array)
    #data = self.global_to_app()
    return array

@app.callback(
    Output("scatter-plot", "figure"), 
    [Input('interval-component', 'n_intervals')],
    Input('intermediate-value', 'data'))
def update_bar_chart(n, data):
    spiral_increment_x = np.array(data[0])
    spiral_increment_y = np.array(data[1])
    #low, high = slider_range
    #mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    print( "data going in graph is:", spiral_increment_x, spiral_increment_y )
    
    fig = px.scatter( df,
        x='x values', y='y values', color ='y values',         
            width=400, height=400)

    fig.update_traces(marker=dict(
        color='blue'))

    fig.add_scatter(x=spiral_increment_x, y=spiral_increment_y)

    fig.update_traces(marker=dict(
        color='red'))
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="LightSteelBlue",
    )
    return fig



def thread_listen_server(): 
    pass

def thread_drone():

    app.run_server(debug=True, 
                host = '0.0.0.0', 
                port=8049,
                #processes = 4,
                #threaded=False
                )
        
#from selenium import webdriver


def sorter(msg):
    global Q
    print("received: ", msg)
    if msg in "LEFTTHUMBUPRIGHT":
        Q.put(msg)


if __name__ == '__main__':

    ### begin INTERCOM
    Q = queue.Queue()
    intercom = dvbcdr.intercom.Intercom()
    intercom.subscribe("hands", sorter)

    ### begin rest
    numRobots = 1
    r = 0.5
    height = 0.3
    final_height = 1.0
    w = 2 * np.pi / numRobots
    T = 2* 2 * np.pi / w 

    URI = 'radio://0/27/2M/E7E7E7E702'#'radio://0/80/2M/E7E7E7E7E7'
    DEFAULT_HEIGHT = 0.3
    DEFAULT_TRANSLATION = 0.3
    is_deck_attached = True

    spiral_points = []
    spiral_absolute = []
    phase =0
    nb_points = 100
    height_increment = height
    for t in np.linspace(0, T, nb_points):
        #height_increment += (final_height - height) / nb_points 
        height_increment = 0
        absolute_pt = [r * np.cos(w * t + phase), r * np.sin(w * t + phase), height_increment]
        spiral_absolute.append (absolute_pt)
        if t != 0:
            t0=t-1
            relative_pt = []
            zip_object = zip(spiral_absolute[-1], spiral_absolute[-2])
            for now_i, before_i in zip_object:
                relative_pt.append(now_i-before_i)
            spiral_points.append (relative_pt)


    spiral_points_x=[]
    spiral_points_y=[]
    spiral_points_z=[]
    for vector3 in spiral_points:
        spiral_points_x.append(vector3[0])
        spiral_points_y.append(vector3[1])
        spiral_points_z.append(vector3[2]) 

    data = {'x values':  spiral_points_x,
            'y values': spiral_points_y,
            }
    import pandas as pd
    df = pd.DataFrame (data, columns = ['x values','y values'])
    print (df)


    spiral_absolute_x=[]
    spiral_absolute_y=[]
    spiral_absolute_z=[]
    for vector3 in spiral_absolute:
        spiral_absolute_x.append(vector3[0])
        spiral_absolute_y.append(vector3[1])
        spiral_absolute_z.append(vector3[2]) 

    global x
    global y
    #x =[]
    #y = []
    #CHANGE THESE AND TRACE UPDATES.
    # spiral_increment_x = [0,1,1,3,2]
    # spiral_increment_y = [0,1,1,4,1.7]
    logging.basicConfig(level=logging.ERROR)    
    # #params = initialize()
    # lock = threading.Lock()

    # # Thread app server.
    # thread_1 = threading.Thread(target=thread_listen_server)
    # thread_1.start()

    # # Thread drone.
    # thread_2 = threading.Thread(target=thread_drone)
    # thread_2.start()

    # thread_1.join()
    # thread_2.join()
    # Run on a separate process so that it doesn't block

    thread_listen_server()
    app_class = Log2App()
    print(app_class.x)
    server_process = multiprocessing.Process(target=thread_drone)
    #server2_process = multiprocessing.Process(target=thread_listen_server)
    server_process.start()
    time.sleep(0.5)
    #server2_process.start()
    #time.sleep(0.5)
    # global app_class
    # app_class = Log2App()

    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                        cb=param_deck_flow)
        time.sleep(1)

        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        #logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)

        logconf.data_received_cb.add_callback(app_class.log_pos_callback)

        if is_deck_attached:
            logconf.start()
            # move_up_and_release(scf)        #drop drone.
            #FF_recover(scf)  #recover from freefall
            # move_square(scf)               
            move_Q(scf)
            #demo_rotation_speeds(scf)       #rotate drone.
            logconf.stop()


    # Visit the dash page
    #driver = webdriver.Firefox()
    #driver.get('http://localhost:8050')
    #time.sleep(0.5)




    

    

