# Stepper: 2048 passos por volta - incremental mapear valor dos analógicos (-1, 1) para valor tunavel (10?)
# Servo: 90 deg aberto e 0 fechado - mapear valor analógico do trigger (-1, 1) para (0, 90)

# Right Trigger (axis 5) -> Servo
# Left Stick Horizontal (axis 0) -> Stepper Angle Base
# Left Stick Vertical (axis 1) -> Stepper Vertical Base
# Right Stick Vertical (axis 3) -> Stepper Vertical Arm

import sys
import serial
import pygame

pygame.init()

uno = serial.Serial(f'/dev/tty{sys.argv[1]}', 115200) # Linux
uno = serial.Serial(f'{sys.argv[1]}', 115200) # Windows

trigger2servo = lambda x: round(-45*x + 45)


def stick2stepper(x):
    drift = 0.01
    power = 10 # still needs some tuning

    if -drift < x < drift: return 0
    else: return round(power*x)


def main():
    joysticks = {}

    done = True
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
    
        for joystick in joysticks.values():

            claw = trigger2servo(joystick.get_axis(5))
            angle = stick2stepper(joystick.get_axis(0))
            base = stick2stepper(joystick.get_axis(1))
            arm = stick2stepper(joystick.get_axis(4))

            values = f"{claw},{angle},{base},{arm}"

            print(values)

            uno.write(values.encode())


if __name__ == "__main__":
    try:
        while True:
            main()

    except (KeyboardInterrupt):
        pygame.quit()
        uno.close()
        quit()
