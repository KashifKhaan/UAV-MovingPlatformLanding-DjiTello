import cv2
import numpy as np
from djitellopy import tello

import POSEESTIMATION
import TRACKING
import GUI

import matplotlib.pyplot as plt
pose = POSEESTIMATION.pose_estimation()
track = TRACKING.track(pose)
window = GUI.gui("1000x700", (650, 450), track)

def initializeTello():
    myDrone = tello.Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone. left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    #myDrone.set_video_resolution(myDrone.RESOLUTION_480P)
    #myDrone.set_video_fps()
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def send_command():
    left_right, far_back, up_down, yaw = track.new_state
    #return 1
    if myDrone.send_rc_control:
        #print("sending")
        myDrone.send_rc_control(left_right, far_back, up_down, yaw)
        return 1
    else:
        return 0
    
def update_parameters():
    window.battery_label.configure(text = "Battery Level: "+str(myDrone.get_battery())+"%")
    window.temperature_label.configure(text = "Temperature: "+str(myDrone.get_temperature())+"C")
    window.altitude_label.configure(text = "Altitude: "+str(myDrone.get_height()))

def plot_data():
    plt.plot(track.x_list)
    plt.plot(track.x_ref_list)
    plt.show()
    

myDrone = initializeTello()

# myDrone.takeoff()
left_right, far_back, up_down, yaw = 0, 0, 0, 0
state = (left_right, far_back, up_down, yaw)
new_state = (left_right, far_back, up_down, yaw)
myFrame = myDrone.get_frame_read()

#cap = cv2.VideoCapture(0)

def main_func():
    if track.land_state == 1:
        print("LANDING")
        track.land_state = -1
        myDrone.land()
        myDrone.end()
        #plot_data()
    if track.send_command_state == 1:
        if send_command():
            track.change_state()
            track.send_command_state = 0
    #ret, frame = cap.read()
    img = myFrame.frame
    img = cv2.flip(img, 0)
    frame = track.update_inputs(img)
    text = str(track.new_state)
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    window.update_video(frame)
    if track.land_state == 0:
        update_parameters()
    window.after(1, main_func)


window.after(0, main_func)
window.mainloop()