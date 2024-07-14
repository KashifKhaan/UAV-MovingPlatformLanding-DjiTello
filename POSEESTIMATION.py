import numpy as np
import cv2
import sys
import yaml
import time


class pose_estimation():

    def __init__(self):

        self.ARUCO_DICT = {
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
    
        self.aruco_type = "DICT_5X5_100"
        self.arucoDict = cv2.aruco.getPredefinedDictionary(self.ARUCO_DICT[self.aruco_type])
        self.arucoParams = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.arucoDict, self.arucoParams)

        self.camera_info = self.get_camera_info(path = 'calibration_matrix.yaml')
        #self.intrinsic_camera = np.array(self.camera_info['camera_matrix'])
        #self.distortion = np.array(self.camera_info['dist_coeff'][0])
        self.matrix_coefficients = np.array(self.camera_info['camera_matrix'])
        self.distortion_coefficients = np.array(self.camera_info['dist_coeff'][0])
        

    def get_camera_info(self, path):
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    
    def estimatePoseSingleMarkers(self, corners, marker_size):
        marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                                [marker_size / 2, marker_size / 2, 0],
                                [marker_size / 2, -marker_size / 2, 0],
                                [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
        trash = []
        rvecs = []
        tvecs = []
        
        for c in corners:
            nada, R, t = cv2.solvePnP(marker_points, c, self.matrix_coefficients, self.distortion_coefficients, False, cv2.SOLVEPNP_IPPE_SQUARE)
            rvecs.append(R)
            tvecs.append(t)
            trash.append(nada)
        return rvecs, tvecs, trash
    
    def get_pose_estimate(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.undistort(gray, self.matrix_coefficients, self.distortion_coefficients, frame)
        corners, ids, rejected_img_points = self.detector.detectMarkers(frame)

            
        if len(corners) > 0:
            for i in range(0, len(ids)):
            
                rvec, tvec, markerPoints = self.estimatePoseSingleMarkers(corners, 100)
                # cv2.aruco.drawDetectedMarkers(frame, corners) 
                for i in range(0, ids.size):
                    cv2.drawFrameAxes(frame, self.matrix_coefficients, self.distortion_coefficients, np.array(rvec)[i, :, :], np.array(tvec)[i, :, :], 50, 2)  
                x, y, z = round(tvec[0][0][0]/10), round(tvec[0][1][0]/10), round(tvec[0][2][0]/10)

                x_ = int((corners[i-1][0][0][0] + corners[i-1][0][1][0] + corners[i-1][0][2][0] + corners[i-1][0][3][0]) / 4)
                y_ = int((corners[i-1][0][0][1] + corners[i-1][0][1][1] + corners[i-1][0][2][1] + corners[i-1][0][3][1]) / 4)
                
                
                return [x_, y_, z], frame
        else:
            return [], frame