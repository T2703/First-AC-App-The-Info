# Author: nono_t27 

import sys
import os
import ac
import acsys
import platform
import configparser

# Magic import stuff to make sure ctypes and sim_info work properly. Gotta learn how to do this better.
if platform.architecture()[0] == "64bit":
    libdir = 'third_party_dir/lib64'
else:
    libdir = 'third_party_dir/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import ctypes
from third_party_dir.sim_info import info
from ctypes.wintypes import MAX_PATH

gear_label = 0 # Label of the gear for the app.
gear = 0 # Current gear for the car.
speed_label = 0 # Label of the speed for the app.
speed = 0 # Speed of the car. 
rpm_label = 0 # Label of the rpm for the app.
rpm = 0 # RPM. 
fuel_label = 0 # Label of the fuel for the app.
fuel = 0 # Fuel of the player's car. 
turbo_label = 0 # Label of the turbo for the app.
turbo = 0 # Turbo boost value of the player's car (if they should have a turbo installed).
ac_user_folder = None # User's folder.
unit_kmh = False # Bool for checking the units.
tire_pressure_label = 0 # Label of the tires pressure for the app. 
tire_pressure_fl =  0 # The pressure for the front left tire.
tire_pressure_fr =  0 # The pressure for the front right tire.
tire_pressure_rl =  0 # The pressure for the rear left tire.
tire_pressure_rr =  0 # The pressure for the rear right tire.
# All of these are correspond to the tires and just shows their pressure.
tire_one = 0 
tire_two = 0
tire_three = 0
tire_four = 0

# The main app window where everything is shown. 
def acMain(ac_version):
   global gear_label, speed_label, rpm_label, unit_kmh, fuel_label, turbo_label, tire_pressure_label
   global tire_one, tire_two, tire_three, tire_four
   
   # Basic app setup.
   appWindow = ac.newApp("The Info")
   ac.setSize(appWindow, 200, 200)

   # Check for the user's units.
   init_ac_folder()
   path = os.path.join(ac_user_folder, "cfg/gameplay.ini")
   speed_unit_config = configparser.ConfigParser()
   speed_unit_config.read(path)

   # If not true then use the MPH other use KMH.
   try:
      unit_kmh = not(bool(int(speed_unit_config.get("OPTIONS", "USE_MPH"))))
   except:
      unit_kmh = True

   # Lables the displays of the things on the app.
   gear_label = ac.addLabel(appWindow, "Gear: N")
   speed_label = ac.addLabel(appWindow, "Speed: 0")
   rpm_label = ac.addLabel(appWindow, "RPM: 0")
   fuel_label = ac.addLabel(appWindow, "Fuel: 0")
   turbo_label = ac.addLabel(appWindow, "Turbo: 0")
   tire_pressure_label = ac.addLabel(appWindow, "Tire Pressures:")
   tire_one = ac.addLabel(appWindow, "1")
   tire_two = ac.addLabel(appWindow, "2")
   tire_three = ac.addLabel(appWindow, "3")
   tire_four = ac.addLabel(appWindow, "4")

   ac.setPosition(gear_label, 3, 30)
   ac.setPosition(speed_label, 3, 50)
   ac.setPosition(rpm_label, 120, 50)
   ac.setPosition(fuel_label, 3, 80)
   ac.setPosition(turbo_label, 120, 80)
   ac.setPosition(tire_pressure_label, 3, 110)
   ac.setPosition(tire_one, 3, 140)
   ac.setPosition(tire_two, 120, 140)
   ac.setPosition(tire_three, 3, 170)
   ac.setPosition(tire_four, 120, 170)
   return "appName"

# Updates the window pretty much the fucntionally goes here.
def acUpdate(deltaT):
   global gear_label, gear, speed_label, speed, rpm_label, rpm, fuel_label, fuel, turbo_label, turbo
   global tire_pressure_fl, tire_pressure_fr, tire_pressure_rl, tire_pressure_rr, tire_one, tire_two, tire_three, tire_four

   gear = ac.getCarState(0, acsys.CS.Gear)
   rpm = ac.getCarState(0, acsys.CS.RPM)
   fuel = info.physics.fuel
   turbo = ac.getCarState(0, acsys.CS.TurboBoost) * 100
   tire_pressure_fl = info.physics.wheelsPressure[0]
   tire_pressure_fr = info.physics.wheelsPressure[1]
   tire_pressure_rl = info.physics.wheelsPressure[2]
   tire_pressure_rr = info.physics.wheelsPressure[3]
   if unit_kmh:
      speed = ac.getCarState(0, acsys.CS.SpeedKMH)
   else:
      speed = ac.getCarState(0, acsys.CS.SpeedMPH)

   # Gear change 
   if gear == 1:
      ac.setText(gear_label, "Gear: N") 
   elif gear == 0:
      ac.setText(gear_label, "Gear: R") 
   else:
      gear += 0
      ac.setText(gear_label, "Gear: {}".format(gear - 1)) 

   # Updating the text by setting them to their current values.
   # If statement for checking the user's units.
   if unit_kmh:
      ac.setText(speed_label, "Speed: {:.0f} KMH".format(speed))
   else:
      ac.setText(speed_label, "Speed: {:.0f} MPH".format(speed))
   

   ac.setText(rpm_label, "RPM: {:.0f}".format(rpm)) 
   ac.setText(fuel_label, "Fuel: {:.0f} liters".format(fuel)) 
   ac.setText(turbo_label, "Turbo: {:.0f}".format(turbo)) 
   ac.setText(tire_one, "FL: {:.0f}".format(tire_pressure_fl))
   ac.setText(tire_two, "FR: {:.0f}".format(tire_pressure_fr))
   ac.setText(tire_three, "RL: {:.0f}".format(tire_pressure_rl))
   ac.setText(tire_four, "RR: {:.0f}".format(tire_pressure_rr))

# Initializes the user's AC folder. 
def init_ac_folder(): 
   global ac_user_folder

   dll = ctypes.windll.shell32
   buf = ctypes.create_unicode_buffer(MAX_PATH + 1)

   if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
      document_folder = buf.value
      ac_folder = os.path.join(document_folder, 'Assetto Corsa')

      if os.path.isdir(ac_folder):
         ac_user_folder = ac_folder
   
# Used for when the application exits. This is here for safety.
def acShutdown():
   return


# ¯\_(ツ)_/¯