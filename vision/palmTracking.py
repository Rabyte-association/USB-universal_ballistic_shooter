import cv2
import mediapipe as mp
from multiprocessing import Process
import imutils

# Declaring MediaPipe objects
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
IMG_W = 1280
IMG_H = 720
class datahold_class:
    data = 1

Data = datahold_class

# Processing the input image
def process_image(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(gray_image)
    # print(results.multi_hand_landmarks)
    return results


# Drawing landmark connections
def draw_hand_connections(img, results):
    if results.multi_hand_landmarks:
        x= results.multi_hand_landmarks[0].landmark[0].x
        y= results.multi_hand_landmarks[0].landmark[0].y
        z= results.multi_hand_landmarks[0].landmark[0].z
        h, w, c = img.shape
        cx, cy = int(x* w), int(y * h)
        print(cx, cy, round(z* 100000, 4))

        # # for handLms in results.multi_hand_landmarks:
        
        # #     for id, lm in enumerate(handLms.landmark):
                
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        return img


def Initialize():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        success, image = cap.read()

        #cv2.imshow("test", image)
       # image = imutils.resize(image, width=1280, height=500)
        results = process_image(image)
        draw_hand_connections(image, results)

        cv2.imshow("Hand tracker", image)

        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()

