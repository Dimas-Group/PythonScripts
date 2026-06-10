import attollo_camera_toolbox as atcam
import thorlabs_s4fc_commands as s4fc
import kohzu_controller_annotated as kohzu
#nimport pg_camera_toolbox as pgcam
import time
#from attollo_live_temp_plotter import start_temperature_plot

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

motors = kohzu.Kohzu_Controller("com21")

def current_motors_positions():
     MOTOR_DICT = {
    "g1_x_tra": 1,
    "g1_y_tra": 2,
    "g1_z_tra": 3,
    "g1_x_rot": 4,
    "g1_y_rot": 5,
    "g1_z_rot": 6,
    "g2_x_tra": 7,
    "g2_y_tra": 8,
    "g2_z_tra": 9,
    "g2_x_rot": 10,
    "g2_y_rot": 11,
    "g2_z_rot": 12,
    "g3_x_tra": 13,
    "g3_y_tra": 14,
    "g3_z_tra": 15,
    "g3_x_rot": 16,
    "g3_y_rot": 17,
    "g3_z_rot": 18,
}
     print("\n--- Current motor positions ---")
     for i in MOTOR_DICT:
          print(f"{i}:", motors.absolute_position_read(i))
          #print(i)

### Put motor adjustments here
#motors.absolute_position_drive("g2_y_rot", 5, 0)
#motors.absolute_position_drive("g1_y_rot", 5, 0)
#motors.absolute_position_drive("g2_y_tra", 5, -20000)
#motors.absolute_position_drive("g1_y_tra", 5, 320000)
#motors.absolute_position_drive("g2_z_tra", 5, 0)



#motors.absolute_position_drive("g1_z_rot", 5, 4000)
#motors.absolute_position_drive("g2_x_rot", 5, 8000)
#motors.absolute_position_drive("g1_x_rot", 5, 8000)



motors.absolute_position_drive("g2_y_tra",5,100000)
motors.absolute_position_drive("g2_y_rot",5,45000)



#motors.absolute_position_drive("g1_z_tra", 5, -2000)

current_motors_positions()