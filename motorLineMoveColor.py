import cv2  # OpenCV를 사용하기위해 import해줍니다.
import numpy as np  # 파이썬의 기본 모듈중 하나인 numpy
from picamera2 import Picamera2
import keyboard
import gpiod
import time

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
    lmotor_in2_line.set_value(0)
    time.sleep(1)
    rmotor_in1_line.set_value(1)
    time.sleep(1)
    rmotor_in2_line.set_value(0)
    time.sleep(1)
    lmotor_en_line.set_value(1)
    time.sleep(1)
    rmotor_en_line.set_value(1)
    time.sleep(1)

def left():
    lmotor_in1_line.set_value(0)
    time.sleep(1)
    lmotor_in2_line.set_value(1)
    time.sleep(1)
    rmotor_in1_line.set_value(0)
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



def main():
    camera = Picamera2()  # 카메라를 비디오 입력으로 사용.
    camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (160, 120)}))
    camera.start()  # 띄울 동영상의 가로사이즈 160픽셀 세로 120픽셀


    while True:  # 카메라가 Open되어 있다면,
        frame = camera.capture_array()   # 비디오의 한 프레임씩 읽습니다.
        frame = cv2.flip(frame, 0)  # 카메라 이미지를 flip, 뒤집습니다. 0은 상하 -1은 좌우로 뒤집는다
        cv2.imshow('normal', frame)  # 'normal'이라는 이름으로 원본 영상을 출력

        crop_img = frame[60:120, 0:160]  # 세로는 60~120픽셀, 가로는 0~160픽셀로 crop(잘라냄)한다.


        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #cv2.IMREAD_COLOR cv2.IMREAD_ANYCOLOR

        # reduce_frame = cv2.pyrDown(gray_frame)
        # reduce_frame = cv2.pyrDown(reduce_frame)

        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([40, 255, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Color Detection', crop_img) # 잘라진 영상 출력

        # 이미지의 윤곽선을 검출
        contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # 윤곽선이 있다면, max(가장큰값)을 반환, 모멘트를 계산한다.
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # X축과 Y축의 무게중심을 구한다.
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # 줄을 따라 움직인다.
            # if cx >= 95 and cx <= 125:
            #     print("Turn Left!")
            #     left()
            #     time.sleep(1)
            #     stop()
            # elif cx >= 39 and cx <= 65:
            #     print("Turn Right")
            #     right()
            #     time.sleep(1)
            #     stop()
            # else:
            #     print("forward")
            #     forward()
            #     time.sleep(1)
            #     stop()

            # X축의 무게중심을 출력한다.
            cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
            cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)

            cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

            print(cx, cy)  # 출력값을 print 한다.

        if cv2.waitKey(1) == ord('q'):  # q값을 누르면 종료
            break

    cv2.destroyAllWindows()  # 화면을 종료한다.




if __name__ == '__main__':
    main()
    lmotor_en_line.release()
    lmotor_in1_line.release()
    lmotor_in2_line.release()
    lmotor_en_line.release()
    lmotor_in1_line.release()
    lmotor_in2_line.release()

