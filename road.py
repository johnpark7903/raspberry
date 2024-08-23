import cv2
import numpy as np

capture = cv2.VideoCapture('images/road2.mp4')

while cv2.waitKey(33) < 0:
    # 동영상 재생이 끝나면 다시 처음부터 재생

    if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = capture.read()

    frame = cv2.pyrDown(frame)
    frame = cv2.pyrDown(frame) #320 x 180

    #print(frame.shape)
    crop_img = frame[160:320, 0:180]
    cv2.imshow("crop", crop_img)

    #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #cv2.IMREAD_COLOR cv2.IMREAD_ANYCOLOR

    #reduce_frame = cv2.pyrDown(gray_frame)
    #reduce_frame = cv2.pyrDown(reduce_frame)

    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 50, 50])
    upper_yellow = np.array([40, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    #cv2.imshow('mask0', mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    #print(contours)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #print(cv2.boundingRect(contour))

    cv2.imshow('Color Detection', crop_img)


    # crop_img = reduce_frame[160:320, 0:180]  # 세로는 60~120픽셀, 가로는 0~160픽셀로 crop(잘라냄)한다.
    #
    # blur = cv2.GaussianBlur(crop_img, (3, 3), 0)  # 가우시안 블러로 블러처리를 한다.
    #
    # ret, thresh1 = cv2.threshold(blur, 177, 255, cv2.THRESH_BINARY_INV)  # 임계점 처리로, 177보다 크면, 255로 변환
    #
    #
    # mask = cv2.erode(thresh1, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    #
    # cv2.imshow('crop', mask)
    #
    # contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # 윤곽선이 있다면, max(가장큰값)을 반환, 모멘트를 계산한다.

    #print(contours)
    #print(cv2.contourArea)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        print(M)
        # X축과 Y축의 무게중심을 구한다.
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # X축의 무게중심을 출력한다.
        cv2.line(mask, (cx, 0), (cx, 720), (255, 0, 0), 1)  #세로선
        cv2.line(mask, (0, cy), (1280, cy), (255, 0, 0), 1) #가로선

        cv2.drawContours(mask, contours, -1, (0, 255, 0), 1)

        #print(cx, cy)  # 출력값을 print 한다.

        cv2.imshow('contour', mask)



capture.release()
cv2.destroyAllWindows()