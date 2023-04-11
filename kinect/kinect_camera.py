import cv2
import freenect
import frame_convert2
def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

while(True):
    frame1=get_depth()
    cv2.imshow('img2',frame1) #display the captured image

    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('depmap.png',frame1)

        cv2.destroyAllWindows()
        break
