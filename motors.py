"""
=============================================================
  MOTOR CONTROL SCRIPT  —  2-PGMI Lab
=============================================================

SETUP
-----
  Run with:  python -i motors.py
  Motors connect automatically on COM9 at 115200 baud.

COMMANDS
--------
  positions()
      Print all 18 motor positions in mm (translation) or
      degrees (rotation). Returns 'no response' if the
      controller does not reply within 0.5 s.

  move(axis, position, speed=5)
      Move a motor to an absolute position. Blocks until
      the move completes or times out (60 s).
        axis     : string name (see AXIS NAMES below)
        position : target in mm (translation) or deg (rotation)
        speed    : integer 1–9, default 5
                   (values outside 1–9 are clamped automatically)
      Examples:
        move("g2_y_rot", -90)          # rotate G2 Y to -90 deg
        move("g1_x_tra", 2.5)          # translate G1 X to 2.5 mm
        move("g3_z_tra", -5, speed=3)

  home(axis, speed=5)
      Send one motor to its hardware origin using the built-in
      magnet/laser sensor. Blocks until complete (max 60 s).
      Example:
        home("g2_y_rot")

  home_all(speed=5)
      Home all 18 motors sequentially.
      WARNING: ensure nothing is obstructing motors before running.

  grating_out(grating)
      Move a grating out of the beam. Saves and returns the
      starting position so it can be restored.
        grating : int or tuple of ints, e.g. 1  or  (1, 2, 3)
      Moves x_tra to -15 mm and y_rot to +90 deg at speed 8.
      Example:
        saved = grating_out(2)

  grating_in(grating, saved=None)
      Move a grating back into the beam.
        grating : int or tuple of ints
        saved   : dict returned by grating_out (optional).
                  If None, returns to origin (0, 0).
      Example:
        grating_in(2, saved)

  save_positions(filename)
      Save all current motor positions to a JSON file.
        filename : path to save file, e.g. "alignment_jan.json"
      Example:
        save_positions("good_alignment.json")

  load_positions(filename, speed=5)
      Move all motors to positions stored in a saved file.
        filename : path to a file created by save_positions()
        speed    : 1–9, default 5
      Example:
        load_positions("good_alignment.json")

AXIS NAMES
----------
  Grating 1:  g1_x_tra  g1_y_tra  g1_z_tra
              g1_x_rot  g1_y_rot  g1_z_rot

  Grating 2:  g2_x_tra  g2_y_tra  g2_z_tra
              g2_x_rot  g2_y_rot  g2_z_rot

  Grating 3:  g3_x_tra  g3_y_tra  g3_z_tra
              g3_x_rot  g3_y_rot  g3_z_rot

CONVERSION FACTORS (steps → physical units)
-------------------------------------------
  x_tra, z_tra :  0.25e-3 mm/step
  y_tra        :  0.05e-3 mm/step
  x_rot, z_rot :  0.60e-3 deg/step
  y_rot        :  2.00e-3 deg/step

APPROXIMATE TRAVEL LIMITS (confirm physically before use)
---------------------------------------------------------
  x_tra, z_tra :  ±15 mm    (±60,000 steps)
  y_tra        :  ±4.75 mm  (±95,000 steps)
  x_rot, z_rot :  ±30 deg   (±50,000 steps)
  y_rot        :  ±90 deg   (±45,000 steps)

=============================================================
"""

import json
import kohzu_controller_annotated as kohzu

COM_PORT = "com9"

motors = kohzu.Kohzu_Controller(COM_PORT)
print(f"Motors connected on {COM_PORT}.")


def positions():
    print("\n--- Current motor positions ---")
    for axis in motors.axis:
        steps = motors.absolute_position_read(axis)
        unit = "deg" if "rot" in axis else "mm"
        if steps == 99999999:
            print(f"  {axis}: no response")
        else:
            converted = int(steps) * motors.axis_units[axis]
            print(f"  {axis}: {converted:.4f} {unit}  ({steps} steps)")


def move(axis, position, speed=5):
    unit = "deg" if "rot" in axis else "mm"
    steps = int(position / motors.axis_units[axis])
    print(f"Moving {axis} to {position} {unit}  ({steps} steps)...")
    motors.absolute_position_drive(axis, speed, steps)
    print(f"  done.")


def home(axis, speed=5):
    print(f"Homing {axis}...")
    motors.absolute_position_origin(axis, speed)
    print(f"  done.")


def home_all(speed=5):
    for axis in motors.axis:
        home(axis, speed)


def grating_out(grating, speed=8):
    saved = motors.move_grating_out(grating)
    print(f"Grating(s) {grating} moved out of beam.")
    return saved


def grating_in(grating, saved=None, speed=8):
    motors.move_grating_in(grating, saved)
    print(f"Grating(s) {grating} moved into beam.")


def save_positions(filename):
    snapshot = {}
    for axis in motors.axis:
        steps = motors.absolute_position_read(axis)
        if steps == 99999999:
            print(f"  WARNING: {axis} returned no response — skipped.")
        else:
            snapshot[axis] = int(steps)
    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Positions saved to '{filename}'.")


def load_positions(filename, speed=5):
    with open(filename) as f:
        snapshot = json.load(f)
    print(f"Loading positions from '{filename}'...")
    for axis, steps in snapshot.items():
        unit = "deg" if "rot" in axis else "mm"
        converted = steps * motors.axis_units[axis]
        print(f"  Moving {axis} to {converted:.4f} {unit}  ({steps} steps)...")
        motors.absolute_position_drive(axis, speed, steps)
    print("All positions restored.")


# Save current positions
home('g2_x_rot')