import socket
import threading
import time
from pyPS4Controller.controller import Controller

# UDP variables
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "10.3.141.1"  # "127.0.0.1" = loopback (send to yourself)
UDP_PORT = 5005
MESSAGE = ""

# L-stick value and R-stick value variables
valL, valR = 0, 0
oldL, oldR = 0, 0
MAX = 32767
DEAD = 4000
DELAY = 30 * (10) ** (-6)

# Direction of rotation variables
FORWARD_L = True
FORWARD_R = True


def mapping(val: float, oldMax: float = MAX, newMax: float = 255):
    """Convert ps4 input value in a PWM readable value (i.e: between 0 and 255)

    Args:
        val (float): initial PS4 input value\n
        oldMax (float, optional): initial max value (here 2**15 - 1). Defaults to MAX.\n
        newMax (float, optional): new max value to fit PWM. Defaults to 255.\n

    Returns:
        int : the equivalent value between 0 and 255
    """
    return int(val * (newMax / oldMax))


class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_square_press(self):
        global MESSAGE
        MESSAGE = "B,1"
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
        time.sleep(DELAY)

    def on_L3_up(self, value):
        if abs(value) >= DEAD:
            global valL, FORWARD_L
            FORWARD_L = True
            valL = abs(mapping(value))
        else:
            valL = 0

    def on_L3_down(self, value):
        if abs(value) >= DEAD:
            global valL, FORWARD_L
            FORWARD_L = False
            valL = abs(mapping(value))
        else:
            valL = 0

    def on_L3_y_at_rest(self):
        global valL
        valL = 0

    def on_R3_up(self, value):
        if abs(value) >= DEAD:
            global valR, FORWARD_R
            FORWARD_R = True
            valR = abs(mapping(value))
        else:
            valR = 0

    def on_R3_down(self, value):
        if abs(value) >= DEAD:
            global valR, FORWARD_R
            FORWARD_R = False
            valR = abs(mapping(value))
        else:
            valR = 0

    def on_R3_y_at_rest(self):
        global valR
        valR = 0

    def on_L2_press(self, value):
        print("on_L2_press: {}".format(value))

    def on_R2_press(self, value):
        print("on_R2_press: {}".format(value))

    # A lot of functions are declared to overwrite them
    # (We could modify the library to prevent this action)
    def on_x_press(self):
        pass

    def on_triangle_press(self):
        pass

    def on_circle_press(self):
        pass

    def on_L1_press(self):
        pass

    def on_R1_press(self):
        pass

    def on_L3_left(self, value):
        pass

    def on_L3_right(self, value):
        pass

    def on_L3_x_at_rest(self):
        pass

    def on_L3_press(self):
        """L3 joystick is clicked. This event is only detected when connecting without ds4drv"""
        print("on_L3_press")

    def on_up_arrow_press(self):
        print("on_up_arrow_press")

    def on_down_arrow_press(self):
        print("on_down_arrow_press")

    def on_left_arrow_press(self):
        print("on_left_arrow_press")

    def on_right_arrow_press(self):
        print("on_right_arrow_press")

    def on_R3_press(self):
        """R3 joystick is clicked. This event is only detected when connecting without ds4drv"""
        print("on_R3_press")

    def on_options_press(self):
        print("on_options_press")

    def on_share_press(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_share_press")

    def on_playstation_button_press(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_playstation_button_press")

    def on_playstation_button_release(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_playstation_button_release")

    def on_x_release(self):
        pass

    def on_triangle_release(self):
        pass

    def on_circle_release(self):
        pass

    def on_square_release(self):
        pass

    def on_L1_release(self):
        pass

    def on_L2_release(self):
        pass

    def on_R2_release(self):
        pass

    def on_R1_release(self):
        pass

    def on_up_down_arrow_release(self):
        pass

    def on_left_right_arrow_release(self):
        pass

    def on_L3_release(self):
        pass

    def on_R3_left(self, value):
        pass

    def on_R3_right(self, value):
        pass

    def on_R3_x_at_rest(self):
        pass

    def on_options_release(self):
        pass

    def on_R3_release(self):
        pass

    def on_share_release(self):
        pass


def InputGet():
    """Open a connection with the PS4 controller. (connecting_using_ds4drv needs to be False)"""
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()


# Create a thread dedicated to collect input values
th_input = threading.Thread(target=InputGet)
th_input.start()

# Continously sending readable instructions to Raspberry Pi with the PS4 inputs
while True:
    if oldL != valL or oldR != valR:
        MESSAGE = str("M,")+str(valL) + ","+(str("A,") if FORWARD_L else str("R,"))+str(valR)+(str(",A") if FORWARD_R else str(",R"))
        oldL = valL
        oldR = valR
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    time.sleep(DELAY)
