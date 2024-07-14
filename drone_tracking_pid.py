import numpy as np
import cv2
import sys
import yaml
import time

from djitellopy import tello


ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    '''
    This will estimate the rvec and tvec for each of the marker corners detected by:
       corners, ids, rejectedImgPoints = detector.detectMarkers(image)
    corners - is an array of detected corners for each detected marker in the image
    marker_size - is the size of the detected markers
    mtx - is the camera matrix
    distortion - is the camera distortion matrix
    RETURN list of rvecs, tvecs, and trash (so that it corresponds to the old estimatePoseSingleMarkers())
    '''
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash


def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    cv2.undistort(gray, matrix_coefficients, distortion_coefficients, frame)


    corners, ids, rejected_img_points = detector.detectMarkers(frame)

        
    if len(corners) > 0:
        for i in range(0, len(ids)):
           
            rvec, tvec, markerPoints = my_estimatePoseSingleMarkers(corners, 100, matrix_coefficients, distortion_coefficients)
            # cv2.aruco.drawDetectedMarkers(frame, corners) 
            for i in range(0, ids.size):
                 cv2.drawFrameAxes(frame, matrix_coefficients, distortion_coefficients, np.array(rvec)[i, :, :], np.array(tvec)[i, :, :], 50, 2)  
            x, y, z = round(tvec[0][0][0]/10), round(tvec[0][1][0]/10), round(tvec[0][2][0]/10)
            s = "     "
            coordinates = str(int(w*x/z)) + s + str(int(h*y/z)) + s + str(z) + s
            # cv2.putText(frame, coordinates, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            x_ = int((corners[i-1][0][0][0] + corners[i-1][0][1][0] + corners[i-1][0][2][0] + corners[i-1][0][3][0]) / 4)
            y_ = int((corners[i-1][0][0][1] + corners[i-1][0][1][1] + corners[i-1][0][2][1] + corners[i-1][0][3][1]) / 4)
            
            
            return [x_, y_, z], frame
    else:
         return [], frame
        

    #return frame

def get_pid_values(coordinates):
    x, y, z = coordinates
    x_ref = 0
    error_x = x_ref - x
    x_out = 0.1 * error_x
    return x_out

def get_velocities(x, y, w, h):

    left_right, far_back, up_down, yaw = 0, 0, 0, 0

    x_center, y_center = w//2, h//2

    kp = 0.5


    left_right = int(np.clip(0.2*(x - x_center), -40, 40))

    up_down = int(np.clip(kp*(y_center - y), -40, 40))

    if (abs(left_right) < 25):
        left_right = 0
    if (abs(up_down) < 25):
        up_down = 0
    
    return left_right, far_back, up_down, yaw

def send_command(left_right, far_back, up_down, yaw):
    if myDrone.send_rc_control:
        myDrone.send_rc_control(left_right, far_back, up_down, yaw)
        return 1
    else:
        return 0

    

def initializeTello():
    myDrone = tello.Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone. left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

aruco_type = "DICT_5X5_100"

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)


# intrinsic_camera = np.array(((933.15867, 0, 657.59),(0,933.1586, 400.36993),(0,0,1)))
# distortion = np.array((-0.43948,0.18514,0,0))



with open('calibration_matrix.yaml', 'r') as file:
    data = yaml.safe_load(file)


intrinsic_camera = np.array(data['camera_matrix'])
distortion = np.array(data['dist_coeff'][0])

cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)



myDrone = initializeTello()
#myDrone.set_video_resolution(myDrone.RESOLUTION_480P)


myDrone.takeoff()
left_right, far_back, up_down, yaw = 0, 0, 0, 0
state = (left_right, far_back, up_down, yaw)
new_state = (left_right, far_back, up_down, yaw)
myFrame = myDrone.get_frame_read()

while True:
    
    img = myFrame.frame
    coordinates, frame = pose_estimation(img, ARUCO_DICT[aruco_type], intrinsic_camera, distortion)
    
    h, w, _ = frame.shape

    p = 0.4

    x_l, x_u = int(p*w), int((1-p)*w)
    y_l, y_u = int(p*h), int((1-p)*h)

    cv2.line(frame, (x_l, 0), (x_l, h), (0, 0, 255), 4)
    cv2.line(frame, (x_u, 0), (x_u, h), (0, 0, 255), 4)
    cv2.line(frame, (0, y_l), (w, y_l), (0, 0, 255), 4)
    cv2.line(frame, (0, y_u), (w, y_u), (0, 0, 255), 4)
    if len(coordinates) > 0:
        x, y, z = coordinates
        cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)
        left_right, far_back, up_down, yaw = get_velocities(x, y, w, h)
        new_state = (left_right, far_back, up_down, yaw)
        if (new_state != state):
            if send_command(left_right, far_back, up_down, yaw):
                state = new_state

    else:
        print("no marker detected")
        left_right, far_back, up_down, yaw = 0, 0, 0, 0
        new_state = (left_right, far_back, up_down, yaw)
        if (new_state != state):
            if send_command(left_right, far_back, up_down, yaw):
                state = new_state

    text = str(state)
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("output", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        myDrone.land()
        myDrone.end()
        break

cap.release()
cv2.destroyAllWindows()