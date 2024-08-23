import cv2

video = cv2.VideoCapture('http://192.168.0.27:4747/mjpegfeed')
frame_size = (640,480)

while True:
    ret, frame = video.read()
    if not ret:
        break

    cv2.imshow('frame', frame)

    # Press 'Esc' to stop
    key = cv2.waitKey(25)
    if key == 27: #ESC
        break

if video.isOpened():
    video.release()
