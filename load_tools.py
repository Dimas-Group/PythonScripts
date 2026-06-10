import attollo_camera_toolbox as atcam
import thorlabs_s4fc_commands as s4fc
import kohzu_controller_annotated as kohzu
#nimport pg_camera_toolbox as pgcam
import time
#from attollo_live_temp_plotter import start_temperature_plot

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

confirm_tuple = ("yes", "Yes", "y", "Y")
attollo_tuple = ("attollo", "Attollo", "a", "A", "at")
pg_tuple = ("Point Grey", "point grey", "Point Gray", "point gray", "pg", "PG")

confirm_tuple = ("yes", "Yes", "y", "Y")
attollo_tuple = ("attollo", "Attollo", "a", "A", "at")
pg_tuple = ("Point Grey", "point grey", "Point Gray", "point gray", "pg", "PG")

if input("Load laser? [n]") in confirm_tuple:
	laser = s4fc.S4FC_Laser("com7")
if input("Load motors? [n]") in confirm_tuple:
	motors = kohzu.Kohzu_Controller("com21")
if input("Load camera? [n]") in confirm_tuple:
    cam_str = input("Attollo or Point-Grey? [Attollo]")
    if cam_str == "":
        cam_str = "a"
    if cam_str in attollo_tuple:
        camera = atcam.AttolloCamera()
        camera.set_gain(3)
        camera.set_exposure(1)
        camera.set_image_dtype(16)

    # if input("Start live temperature monitor? [n]") in confirm_tuple:
    #         print("Starting temperature plot in a non-blocking window...")
    #         # Store 'ani' to keep the animation running
    #         ani = start_temperature_plot(camera)
    #         print("Plot window is running. You can continue to use the terminal.")

print("\n--- Hardware setup complete ---")
#print("Initialized objects: laser, motors, camera, ani")
#print("Type 'camera.close()' and 'motors.close()' when finished.")

# -------------- 2PGMI -------------- # 

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


# motors.absolute_position_origin("g3_x_rot", 5)
# current_motors_positions()
# motors.absolute_position_drive("g2_y_tra", 2, -95_000)
#motors.absolute_position_origin("g2_y_tra",2)
# # motors.absolute_position_drive("g1_x_tra", 3, 50_000)
# # motors.absolute_position_drive("g1_z_rot", 4,25_000)
# # motors.absolute_position_drive("g1_y_rot", 4, 45_000)
# # motors.absolute_position_origin("g1_y_rot",4)
# # time.sleep(0.5)
# # motors.absolute_position_origin("g1_z_rot",4)
# # time.sleep(0.5)
# # motors.absolute_position_origin("g1_x_tra",4)

# motors.absolute_position_drive("g1_z_tra", 4, 10_000)
# time.sleep(0.5)
# motors.absolute_position_drive("g1_z_tra", 4, 50900)

#motors.absolute_position_drive("g1_z_tra", 4, 10000)





















#current_motors_positions()

#motors.absolute_position_origin("g1_x_tra", 5)
#before = camera.return_image()
#motors.absolute_position_drive("g3_z_tra", 8, 40000)

#g1_pos = np.arange(-50_000 , 50_000 + 1, 1_000)

#motors.absolute_position_origin("g3_z_tra", 8)
#motors.absolute_position_drive("g1_z_tra", 8, 50_000)
#time.sleep(0.5)
#motors.absolute_position_drive("g3_z_tra", 8, 10_000)
#motors.absolute_position_drive("g1_x_tra", 8, 50_000)
# motors.absolute_position_drive("g1_z_rot", 6, 20_000)
# time.sleep(0.5)
# motors.absolute_position_drive("g2_z_rot", 6, -20_000)
# time.sleep(0.5)
# motors.absolute_position_drive("g3_z_rot", 6, 20_000)

#motors.absolute_position_drive("g1_z_rot", 8, 0)



# def move_gratings_out_of_beam():
#     motors.absolute_position_drive("g1_y_rot", 8, 45_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g2_y_rot", 8, 45_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g3_y_rot", 8, 0)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g1_x_tra", 8,50_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g2_x_tra", 8,-50_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g3_x_tra", 8,70_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g1_z_rot", 8, 20_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g2_z_rot", 6, -20_000)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g3_z_rot", 6, 20_000)


# def move_gratings_back_in_beam():
#     motors.absolute_position_origin("g1_z_rot", 8)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g2_z_rot", 8)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g3_z_rot", 8)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g1_y_rot", 8)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g2_y_rot", 8)
#     time.sleep(0.5)
#     motors.absolute_position_drive("g3_y_rot", 8, 45_000)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g1_x_tra", 8)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g2_x_tra", 8)
#     time.sleep(0.5)
#     motors.absolute_position_origin("g3_x_tra", 8)


# motors.absolute_position_drive("g2_y_rot", 3, int(-2250))


# ---------------- Move grating 2 out of the beam ---------------- #
# to put back bring "g2_y_rot" back to 0

# #y_rot_steps = np.linspace(0, -45_000, 21)
# y_rot_steps = np.linspace(-45_000, 0, 21)
# #print(y_rot_steps)
# for i in y_rot_steps:
#     print(i*2e-3, "degrees")
#     motors.absolute_position_drive("g2_y_rot", 2, int(i))
#     time.sleep(0.5)

# ---------------- Move grating 1 out of the beam ---------------- #
# to put back bring "g1_y_rot" back to 0

# y_rot_steps = np.linspace(0, 45_000, 21)
# y_rot_steps = np.linspace(45_000, 0, 21)
# # motors.absolute_position_drive("g1_y_rot", 2, int(2250))
# print(y_rot_steps)
# for i in y_rot_steps:
#     print(i*2e-3, "degrees")
#     motors.absolute_position_drive("g1_y_rot", 2, int(i))
#     time.sleep(0.5)

# motors.absolute_position_origin("g1_z_rot", 3)
# motors.absolute_position_origin("g1_y_rot", 3)
# motors.absolute_position_origin("g1_x_rot", 3)

# motors.absolute_position_drive("g1_x_rot", 5, 0)
#motors.absolute_position_drive("g2_x_rot", 5, 0)
#motors.absolute_position_drive("g1_y_rot", 5, 0)
#motors.absolute_position_drive("g2_y_rot", 5, 0)
#motors.absolute_position_drive("g1_z_rot", 5, 0) ####
#motors.absolute_position_drive("g2_z_rot", 5, 0) ####

# time.sleep(0.5)
# motors.absolute_position_drive("g1_x_rot", 3, 0)
# motors.absolute_position_drive("g1_z_rot", 3, -2000)
# motors.absolute_position_drive("g2_z_rot", 3, 2000)



# laser.enable_laser()
# laser.lock_off()
# laser.set_laser_output(2)
# laser.lock_on()
# time.sleep(1)
# print(laser.read_laser_output())

# laser.disable_laser()

# im = camera.return_image()
# save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
# np.save(save_path + r"\grating_400um_test_0" , im)

# time.sleep(0.5)

# #----------------------------#
# tra_z_steps = np.linspace(50000,-50000, 51)
# # rot_steps = np.linspace(-5_000,5_000, 101)
# # motors.absolute_position_drive("g1_z_tra", 3, 50000)
# # time.sleep(0.5)
# # motors.absolute_position_drive("g2_z_tra", 3, 50000)
# for i in tra_z_steps:
     
#     motors.absolute_position_drive("g1_z_tra", 5, int(i))
#     time.sleep(0.5)
#     im = camera.return_image()
#     save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
#     np.save(save_path + r"\tra_z_g1_"+f"{i}_g2_50000.0" , im)
#     print("done G1:", i)

# time.sleep(0.5)

# for i in tra_z_steps:
#     motors.absolute_position_drive("g2_z_tra", 5, int(i))
#     time.sleep(0.5)
#     im = camera.return_image()
#     save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
#     np.save(save_path + r"\tra_z_g1_"+f"-50000.0_g2_{i}.0" , im)
#     print("done G2:", i)
#print(rot_steps)
# motors.absolute_position_drive("g1_z_rot", 5, -100)
# time.sleep(0.5)
# motors.absolute_position_drive("g1_x_tra", 5, -5_000)
#motors.absolute_position_origin("g3_y_rot", 5)
#motors.absolute_position_drive("g3_x_tra", 7, 0)
#motors.absolute_position_origin("g3_z_rot", 5)
# for i in rot_steps:
#     motors.absolute_position_drive("g1_z_rot", 5, int(i))
#     time.sleep(0.5)
#     im = camera.return_image()
#     save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
#     np.save(save_path + r"\g1_rot_"+f"{i}" , im)
#     print("done:", i)

# motors.absolute_position_drive("g3_y_tra", 5, 50_000)


#motors.absolute_position_drive("g1_x_tra", 2, 5_000)
# x_tra_steps = np.linspace(-10_000,10_000, 51)
# print(x_tra_steps)
# for i in x_tra_steps:
#     motors.absolute_position_drive("g1_x_tra", 5, int(i))
#     time.sleep(0.5)
#     im = camera.return_image()
#     save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
#     np.save(save_path + r"\g1_x_tra_"+f"{i}" , im)
#     print("done:", i)

# y_tra_steps = np.linspace(-10_000,10_000, 51)
# print(y_tra_steps)
# for i in y_tra_steps:
#     motors.absolute_position_drive("g1_y_tra", 5, int(i))
#     time.sleep(0.5)
#     im = camera.return_image()
#     save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
#     np.save(save_path + r"\g1_y_tra_"+f"{i}" , im)
#     print("done:", i)

# Save background noise
# im = camera.return_image()
# save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
# np.save(save_path + r"\noise" , im)

current_motors_positions()
# tra_y_steps = np.linspace(-20_000,20_000, 51)

# for i in tra_y_steps:
#     motors.absolute_position_drive("g1_y_tra", 5, int(i))
#     time.sleep(0.5)
#     im = camera.return_image()
#     save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
#     np.save(save_path + r"\g1_tra_y_"+f"{i}" , im)
#     print("done:", i)




# im = camera.return_image()
# save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
# np.save(save_path + r"\g1_rot_"+f"test_0" , im)
# time.sleep(0.5)
# motors.absolute_position_origin("g1_y_rot", 8)
# time.sleep(0.5)

# # # motors.absolute_position_drive("g1_z_tra", 8, 52_000)
# # # motors.absolute_position_drive("g2_z_tra", 8, 52_000)

# time.sleep(0.5)
# motors.absolute_position_drive("g1_z_rot", 1, 0)
# motors.absolute_position_drive("g1_z_tra", 4, 50_000)
# time.sleep(0.5)
# motors.absolute_position_drive("g2_z_tra", 4, 50_000)
#camera.return_temp()


# print("done")

# laser.enable_laser()
# laser.lock_off()
# laser.set_laser_output(2)
# laser.lock_on()

# print(laser.read_laser_output())

# im = camera.return_image()
# save_path = r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\2-PGMI-alignment"
# np.save(save_path + r"\test0" , im)
# time.sleep(0.5)
# camera.close()
# # laser.disable_laser()
#     # # motors.absolute_position_origin("g1_z_tra", 8)
# print("Done.")

# print("file saved as:", save_path + r"\test0.npy" )
# im = np.load(save_path + r"\test0.npy")
# plt.imshow(im)
# plt.show()
#----------------------------#
# carpet = []
# Grating 1
# motors.absolute_position_origin("g1_z_rot", 8)
# time.sleep(0.5)
# motors.absolute_position_origin("g1_y_rot", 8)
# time.sleep(0.5)
# motors.absolute_position_origin("g1_x_tra", 8)
# time.sleep(0.5)
# for z in g1_pos:
#       print("g1_z_tra:", z)
#       motors.absolute_position_drive("g1_z_tra", 8, z)
#       print(motors.absolute_position_read("g1_z_tra"))
#       time.sleep(0.5)

#       im = camera.return_image()
#       carpet.append(im[0])
      #np.save(r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\3-PGMI-test_3" + f"\g1_z_tra_{z}", im)
# im = camera.return_image()
# np.save(r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR\3-PGMI_4f_alignment" + r"\test_3" , im)
# camera.close()
# laser.disable_laser()
# print("Done.")

# time.sleep(0.5)
# print("Loop done \n Back to origin")
# #motors.absolute_position_origin("g1_y_rot", 8)
# #time.sleep(0.5)
# #motors.absolute_position_origin("g3_z_tra", 8)

# plt.imshow(im)
# plt.show()


# print(motors.absolute_position_read("g1_z_tra"))
# motors.absolute_position_drive("g1_z_tra", 8, 10_000)
# laser.enable_laser()
# laser.lock_off()
# time.sleep(3)
# print(laser.read_laser_output())
# laser.set_laser_output(20)
# print(laser.read_laser_output())
# print(laser.read_laser_temperature())
# im = camera.return_image()
# camera.save_image("NIR-test_1")
# laser.disable_laser()
# camera.close()
# print(motors.absolute_position_read("g1_z_tra"))
# motors.absolute_position_origin("g1_z_tra", 8)
# filename= "test_1"
#np.save(r"C:\Users\Dima's group\Documents\Python Scripts\Nir-IR" + f"\{filename}", im)
# plt.imshow(im)
# plt.show()