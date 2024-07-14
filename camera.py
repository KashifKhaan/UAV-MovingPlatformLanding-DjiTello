from djitellopy import Tello
import cv2
drone = Tello()
import time

drone.connect()

drone.send_command_with_return("downvision 1")
drone.streamon()
index = 1
#img = cv2.VideoCapture(0)
# drone.set_video_direction(Tello.CAMERA_DOWNWARD)
while True:

    # IsTrue, frame = img.read()
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, (360, 240))
    myFrame = drone.get_frame_read()
   
    frame = myFrame.frame
    dframe = cv2.flip(frame, 0)

    cv2.imshow("Image", dframe)

    cond = cv2.waitKey(10) & 0xFF

    if cond == ord('d'):
        seconds = 1672215379.5045543
        local_time = time.ctime(seconds)
        path = "C:\\Users\\Nabeel Ahmad\\Documents\\Telllo\\18_05_2024\images\\img" + str(index) + ".jpeg"
        index +=1
        cv2.imwrite(path, frame)

    elif cond == ord('e'):
        break  
