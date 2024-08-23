import gpiod
import time
import keyboard

def forward():
    lmotor_in1_line.set_value(1)
    time.sleep(1)
    lmotor_in2_line.set_value(0)
    time.sleep(1)
    rmotor_in1_line.set_value(0)
    time.sleep(1)
    rmotor_in2_line.set_value(1)
    time.sleep(1)
    lmotor_en_line.set_value(1)
    time.sleep(1)
    rmotor_en_line.set_value(1)
    time.sleep(1)

def reverse():
    lmotor_in1_line.set_value(0)
    time.sleep(1)
    lmotor_in2_line.set_value(1)
    time.sleep(1)
    rmotor_in1_line.set_value(1)
    time.sleep(1)
    rmotor_in2_line.set_value(0)
    time.sleep(1)
    lmotor_en_line.set_value(1)
    time.sleep(1)
    rmotor_en_line.set_value(1)
    time.sleep(1)

def stop():
    lmotor_in1_line.set_value(1)
    time.sleep(1)
    lmotor_in2_line.set_value(1)
    time.sleep(1)
    rmotor_in1_line.set_value(1)
    time.sleep(1)
    rmotor_in2_line.set_value(1)
    time.sleep(1)
    lmotor_en_line.set_value(1)
    time.sleep(1)
    rmotor_en_line.set_value(1)
    time.sleep(1)

def right():
    lmotor_in1_line.set_value(1)
    time.sleep(1)
    lmotor_in2_line.set_value(1)
    time.sleep(1)
    rmotor_in1_line.set_value(1)
    time.sleep(1)
    rmotor_in2_line.set_value(1)
    time.sleep(1)
    lmotor_en_line.set_value(1)
    time.sleep(1)
    rmotor_en_line.set_value(1)
    time.sleep(1)

def left():
    lmotor_in1_line.set_value(1)
    time.sleep(1)
    lmotor_in2_line.set_value(1)
    time.sleep(1)
    rmotor_in1_line.set_value(1)
    time.sleep(1)
    rmotor_in2_line.set_value(1)
    time.sleep(1)
    lmotor_en_line.set_value(1)
    time.sleep(1)
    rmotor_en_line.set_value(1)
    time.sleep(1)


LMOTOR_EN = 26
LMOTOR_IN1 = 19
LMOTOR_IN2 = 13
RMOTOR_EN = 0
RMOTOR_IN1 = 5
RMOTOR_IN2 = 6

# SW = 12

chip = gpiod.Chip('gpiochip4')
# sw_line = chip.get_line(SW)
# sw_line.request(consumer ="switch" ,type=gpiod.LINE_REQ_DIR_IN)
lmotor_en_line = chip.get_line(LMOTOR_EN)
lmotor_en_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
lmotor_in1_line = chip.get_line(LMOTOR_IN1)
lmotor_in1_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
lmotor_in2_line = chip.get_line(LMOTOR_IN2)
lmotor_in2_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
rmotor_en_line = chip.get_line(RMOTOR_EN)
rmotor_en_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
rmotor_in1_line = chip.get_line(RMOTOR_IN1)
rmotor_in1_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
rmotor_in2_line = chip.get_line(RMOTOR_IN2)
rmotor_in2_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        while True:
            if keyboard.is_pressed('w'):
                forward()
            elif keyboard.is_pressed('s'):
                reverse()
            elif keyboard.is_pressed('a'):
                left()
            elif keyboard.is_pressed('d'):
                right()
            elif keyboard.is_pressed('x'):
                stop()
            elif keyboard.is_pressed('q'):
                break
finally:
    lmotor_en_line.release()
    lmotor_in1_line.release()
    lmotor_in2_line.release()
    lmotor_en_line.release()
    lmotor_in1_line.release()
    lmotor_in2_line.release()