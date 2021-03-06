import pygame

import tools

import config as c

try:
    import RPi.GPIO as GPIO
    tools.Debug_Print("GPIO setup was successful.")
except:
    print ("Could not import RPi.GPIO")
    tools.Debug_Print("Could not import RPi.GPIO.")

class Rod:

    allowed_to_move = False

    limit_left_up    = False
    limit_left_down  = False
    limit_right_up   = False
    limit_right_down = False

    # If servo code were reimplemented completely,
    # this should be set to True
    servos_operational = True

    left_bar_position  = 260
    right_bar_position = 260


    def __init__(self, config):
        self.config = config

        # Sets up GPIO pins and motors - DO NOT MODIFY
        c.LeftServoStatus = "Setup Failed!"
        c.RightServoStatus = "Setup Failed!"
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(int(self.config['Servos']['RPiPinLeftServo']), GPIO.OUT)
            GPIO.setup(int(self.config['Servos']['RPiPinRightServo']), GPIO.OUT)

            self.left_servo  = GPIO.PWM(int(self.config['Servos']['RPiPinLeftServo']), 50)
            c.LeftServoStatus = "Setup Successful"
            self.right_servo = GPIO.PWM(int(self.config['Servos']['RPiPinRightServo']), 50)
            c.RightServoStatus = "Setup Successful"
            tools.Debug_Print("Servo setup was successful.")
        except:
            print ("Could not set up servos.")
            tools.Debug_Print("Could not set up servos.")
            servos_operational = False


    def activate_joysticks(self, pressed_keys):

        # Setting this to stop motors when not pressed - remove when code accomodates stoping motors
        self.player_move(0,0)

        if pressed_keys[self.config['Controls']['JoyLeftUp']] and pressed_keys[self.config['Controls']['JoyRightUp']]:
            self.player_move(1, 1)
        elif pressed_keys[self.config['Controls']['JoyLeftUp']] and pressed_keys[self.config['Controls']['JoyRightDown']]:
            self.player_move(1, -1)
        elif pressed_keys[self.config['Controls']['JoyLeftDown']] and pressed_keys[self.config['Controls']['JoyRightUp']]:
            self.player_move(-1, 1)
        elif pressed_keys[self.config['Controls']['JoyLeftDown']] and pressed_keys[self.config['Controls']['JoyRightDown']]:
            self.player_move(-1, -1)
        elif pressed_keys[self.config['Controls']['JoyLeftUp']]:
            self.player_move(1, 0)
        elif pressed_keys[self.config['Controls']['JoyLeftDown']]:
            self.player_move(-1, 0)
        elif pressed_keys[self.config['Controls']['JoyRightUp']]:
            self.player_move(0, 1)
        elif pressed_keys[self.config['Controls']['JoyRightDown']]:
            self.player_move(0, -1)


    """
    Formula to drive servos
    ----------------------------------
    * The midpoint (stalling point) for the continuous servo is 7.5
    * While the stalling point should be the midpoint, the servo must be calibrated properly, so alternatively setting the pulse to 0 will stop movement
    * Full speed one direction is 5 (min)
    * Full speed the other direction is 10 (max)
    * Slower speeds are achievable at values between midpoint and min/max.
    """
    def move(self, left, right, add_sound = False):
        if left > 0:
            if self.limit_left_up:
                print('LEFT UP PREVENTED!')
                tools.Debug_Print('LEFT UP PREVENTED!')
            else:
                print('Moving left up!')
                tools.Debug_Print('Moving left up!')
                if add_sound: tools.play_sound(self.config['Audio']['RodLeftUp'])

                if self.servos_operational:
                    try:
                        self.left_servo.start(7.5 + self.config['Servos']['SpeedLeftUp'])
                    except:
                        print('ERROR: Could not move left servo up.')
                        tools.Debug_Print('ERROR: Could not move left servo up.')

                # This is superficial, for testing purposes. Will be removed.
                self.left_bar_position -= 3

        elif left < 0:
            if self.limit_left_down:
                print('LEFT DOWN PREVENTED!')
                tools.Debug_Print('LEFT DOWN PREVENTED!')
            else:
                print('Moving left down!')
                tools.Debug_Print('Moving left down!')
                if add_sound: tools.play_sound(self.config['Audio']['RodLeftDown'])

                if self.servos_operational:
                    try:
                        self.left_servo.start(7.5 - self.config['Servos']['SpeedLeftDown'])
                    except:
                        print('ERROR: Could not move left servo down.')
                        tools.Debug_Print('ERROR: Could not move left servo down.')

                # This is superficial, for testing purposes. Will be removed.
                self.left_bar_position += 3

        else:
            if self.servos_operational:
                try:
                    #setting pulse to 0 to kill motor rather than 7.5 to stall it
                    self.left_servo.start(0)
                except:
                    print('ERROR: Could not stop left servo.')
                    tools.Debug_Print('ERROR: Could not stop left servo.')


        if right > 0:
            if self.limit_right_up:
                print('RIGHT UP PREVENTED!')
                tools.Debug_Print('RIGHT UP PREVENTED!')
            else:
                print('Moving right up!')
                tools.Debug_Print('Moving right up!')
                if add_sound: tools.play_sound(self.config['Audio']['RodRightUp'])

                if self.servos_operational:
                    try:
                        self.right_servo.start(7.5 - self.config['Servos']['SpeedRightUp'])
                    except:
                        print('ERROR: Could not move right servo up.')
                        tools.Debug_Print('ERROR: Could not move right servo up.')

                # This is superficial, for testing purposes. Will be removed.
                self.right_bar_position -= 3

        elif right < 0:
            if self.limit_right_down:
                print('RIGHT DOWN PREVENTED!')
                tools.Debug_Print('RIGHT DOWN PREVENTED!')
            else:
                print('Moving right down!')
                tools.Debug_Print('Moving right down!')
                if add_sound: tools.play_sound(self.config['Audio']['RodRightDown'])

                if self.servos_operational:
                    try:
                        self.right_servo.start(7.5 + self.config['Servos']['SpeedRightDown'])
                    except:
                        print('ERROR: Could not move right servo down.')
                        tools.Debug_Print('ERROR: Could not move right servo down.')

                # This is superficial, for testing purposes. Will be removed.
                self.right_bar_position += 3

        else:
            if self.servos_operational:
                try:
                    #setting pulse to 0 to kill motor rather than 7.5 to stall it
                    self.right_servo.start(0)
                except:
                    print('ERROR: Could not stop right servo.')
                    tools.Debug_Print('ERROR: Could not stop right servo.')


    def player_move(self, left, right):
        if self.allowed_to_move:
            self.move(left, right, True)
        else:
            print('NOT ALLOWED TO MOVE RIGHT NOW!')
            tools.Debug_Print('NOT ALLOWED TO MOVE RIGHT NOW!')


    def generate_graphics(self, screen):
        """ This is superficial, for testing purposes. Will be removed. """

        # Set the left and right carriages to blue
        left_block_color  = (0, 128, 255)
        right_block_color = (0, 128, 255)

        # If a limit switch is active on either side, change its carriage to orange
        if self.limit_left_up  or self.limit_left_down or not self.allowed_to_move:  left_block_color  = (255, 100, 0)
        if self.limit_right_up or self.limit_right_down or not self.allowed_to_move: right_block_color = (255, 100, 0)

        # Draw the carriages to the screen
        pygame.draw.rect(screen, left_block_color,  pygame.Rect(90,  self.left_bar_position,  60, 60))
        pygame.draw.rect(screen, right_block_color, pygame.Rect(490, self.right_bar_position, 60, 60))

        # Add a line for the bar between the carriage blocks
        pygame.draw.line(screen, (200, 200, 200), (150, self.left_bar_position + 30), (490, self.right_bar_position + 30), 10)
