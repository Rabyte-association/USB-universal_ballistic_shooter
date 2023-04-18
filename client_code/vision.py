import cv2
import threading

value = (-0.33,0)
W, H = 1280, 720

def InitializeVideo(value):
    cap = cv2.VideoCapture("http://usb.local/stream")
    while True:
        _, frame = cap.read()
        new_value = (int((1+value[0])*(W/2)), int((1-value[1])*(H/2)))
        a, b = 255,300
        c = (255,300)
        frame = cv2.arrowedLine(frame, (int(W/2), int(H/2)), new_value, (0,255,0), int(2))
        #frame = cv2.line(frame, new_value, new_value, (0,255,0), int(2))

        cv2.imshow('sas', frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

if __name__ == "__main__":
    video = threading.Thread(target=InitializeVideo, args=[value])
    video.start()