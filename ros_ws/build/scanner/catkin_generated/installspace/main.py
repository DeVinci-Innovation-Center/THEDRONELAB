#!/usr/bin/env python3
import argparse
import yaml
import os
import subprocess
import numpy as np
import re
import time
import threading

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.position_hl_commander import PositionHlCommander as phm
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--configpath",
        type=str,
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../launch/"),
        help="Path to the configuration *.yaml files")
    parser.add_argument(
        "--stm32Fw",
        type=str,
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../crazyflie-firmware/cf2.bin"),
        help="Path to cf2.bin")
    parser.add_argument(
        "--nrf51Fw",
        type=str,
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../crazyflie2-nrf-firmware/cf2_nrf.bin"),
        help="Path to cf2_nrf.bin")
    args = parser.parse_args()

    if not os.path.exists(os.path.join(args.configpath, "allCrazyflies.yaml")) or \
        not os.path.exists(os.path.join(args.configpath, "crazyflieTypes.yaml")) or \
        not os.path.exists(os.path.join(args.configpath, "crazyflies.yaml")):
        print("ERROR: Could not find all yaml configuration files in configpath ({}).".format(args.configpath))
        exit()

    if not os.path.exists(args.stm32Fw):
        print("WARNING: Could not find STM32 firmware ({}).".format(args.stm32Fw))

    if not os.path.exists(args.nrf51Fw):
        print("WARNING: Could not find NRF51 firmware ({}).".format(args.nrf51Fw))

    # read a yaml file
    def read_by_id(path):
        by_id = {}
        with open(path, 'r') as ymlfile:
            root = yaml.load(ymlfile)
            for node in root["crazyflies"]:
                id = int(node["id"])
                by_id[id] = node
        return by_id

    def selected_cfs():
        global goodresponse
        # TODO change this to scan available 
        nodes = [node for id, node in allCrazyflies.items() if bool(goodresponse[id])]
        return nodes

    def save():
        nodes = selected_cfs()
        print("beging saving")
        with open(os.path.join(args.configpath, "crazyflies.yaml"), 'w') as outfile:
            yaml.dump({"crazyflies": nodes}, outfile)
        print("saved !!!")

    def initpos():
        cflib.crtp.init_drivers()
        nodes = selected_cfs()
        for n in nodes:
            # print(n)
            # add = (str(n["id"])).rjust(2,'0')
            # URI = uri_helper.uri_from_env(default=f'radio://0/27/2M/E7E7E7E7{add}')
            # print(URI)

            # with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
            #     with phm(scf) as heer:
            #         heer.land()
            #         pos = heer.get_position()
            #         print(pos)
<<<<<<< HEAD
            n['initialPosition']=[]
=======
            n['initialPosition'] = []
>>>>>>> 5085894d031e7056fccd4fdd06b2ae0a1d14e09e
            n['initialPosition'].append(0.00)
            n['initialPosition'].append(0.00)
            n['initialPosition'].append(0.00)

    def checkBattery():
            # query each CF
            global goodresponse
            nodes = selected_cfs()
            for crazyflie in nodes:
                id = "{0:02X}".format(crazyflie["id"])
                uri = "radio://0/{}/2M/E7E7E7E7{}".format(crazyflie["channel"], id)
                cfType = crazyflie["type"]
                bigQuad = cfTypes[cfType]["bigQuad"]

                try:
                    if not bigQuad:
                        voltage = subprocess.check_output(["rosrun crazyflie_tools battery --uri " + uri], shell=True)
                    else:
                        voltage = subprocess.check_output(["rosrun crazyflie_tools battery --uri " + uri + " --external 1"], shell=True)
                except subprocess.CalledProcessError:
                    voltage = None  # CF not available

                color = '#000000'
                status = "OK !"
                if voltage is not None:
                    voltage = float(voltage)
                    if voltage < cfTypes[cfType]["batteryVoltageWarning"]:
                        color = '#FF8800'
                        status = "WARN"
                        goodresponse[crazyflie["id"]] = False
                    if voltage < cfTypes[cfType]["batteryVoltateCritical"]:
                        color = '#FF0000'
                        status = "CRIT"
                        goodresponse[crazyflie["id"]] = False
                    widgetText = "{:.2f} v".format(voltage)
                else:
                    widgetText = "Err"
                    status = "OUPS"
                    goodresponse[crazyflie["id"]] = False
                print(f'{crazyflie["id"]}===> {widgetText} | {status}')
            # widgets[crazyflie["id"]].batteryLabel.config(foreground=color, text=widgetText)
    global goodresponse
    allCrazyflies = read_by_id(os.path.join(args.configpath, "allCrazyflies.yaml"))
    goodresponse = np.ones(len(allCrazyflies.items())+1)
    enabled = read_by_id(os.path.join(args.configpath, "crazyflies.yaml")).keys()
    with open(os.path.join(args.configpath, "crazyflieTypes.yaml"), 'r') as ymlfile:
        data = yaml.load(ymlfile)
        cfTypes = data["crazyflieTypes"]
    checkBattery()
    initpos()
    save()
    
    


