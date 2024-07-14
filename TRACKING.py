import cv2
import numpy as np

class track():

    def __init__(self, pose):
        self.pose = pose
        self.left_right = 0
        self.far_back = 0
        self.up_down = 0
        self.yaw = 0
        self.button_check = 0
        self.land_state = 0
        self.send_command_state = 0
        self.trackandland = 0
        self.x_list, self.x_ref_list, self.y_list, self.y_ref_list = [], [], [], []

        self.error_x, self.error_y, self.prev_error_z = 0, 0, 0
        self.prev_error_x, self.prev_error_y , self.prev_error_z = self.error_x, self.error_y, self.prev_error_z


        self.state = (self.left_right, self.far_back, self.up_down, self.yaw)
        self.new_state = self.state

    def change_state(self):
        self.state = (self.left_right, self.far_back, self.up_down, self.yaw)

    def change_new_state(self):
        self.new_state = (self.left_right, self.far_back, self.up_down, self.yaw)

    def update_velocities(self, x, y, z, x_ref, y_ref, z_ref):

        """self.x_list.append(x)
        self.x_ref_list.append(x_ref)
        self.y_list.append(y)
        self.y_ref_list.append(y_ref)"""

        self.left_right, self.far_back, self.up_down, self.yaw = 0, 0, 0, 0

        speed = 100
        self.error_x, self.error_y, self.error_z = x - x_ref, y_ref - y, z_ref - z

        p, d = 0.1, 0.65

        self.left_right = int(np.clip(p*self.error_x + d*(self.error_x - self.prev_error_x), -speed, speed))
        self.far_back = int(np.clip(p*self.error_y + d*(self.error_y - self.prev_error_y), -speed, speed))

        self.prev_error_x, self.prev_error_y = self.error_x, self.error_y


        """if abs(self.left_right) < 10:
            self.left_right = 0
        if abs(self.far_back) < 10:
            self.far_back = 0 """

        if abs(self.left_right) < 25 and abs(self.far_back) < 25 and self.trackandland == 1:
            if z < z_ref + 10:
                self.land_state = 1
            else:   
                #self.up_down = int(np.clip(0.4*self.error_z + 0.4*(self.error_z - self.prev_error_z), -60, 60))
                #self.prev_error_z = self.error_z
                self.up_down = -40
        else:
            self.up_down = 0        

    def update_inputs(self, frame):
        if self.land_state == 0:
            if not self.button_check:
                coordinates, frame = self.pose.get_pose_estimate(frame)
                h, w, _ = frame.shape
                x_ref, y_ref, z_ref = w//2, h//2, 80
                p = 0.30
                x_l, x_u = int(p*w), int((1-p)*w )
                y_l, y_u = int(p*h), int((1-p)*h)

                cv2.line(frame, (x_l, 0), (x_l, h), (255, 0, 0), 4)
                cv2.line(frame, (x_u, 0), (x_u, h), (255, 0, 0), 4)
                cv2.line(frame, (0, y_l), (w, y_l), (255, 0, 0), 4)
                cv2.line(frame, (0, y_u), (w, y_u), (255, 0, 0), 4)
                if len(coordinates) > 0:
                    x, y, z = coordinates
                    print(z)
                    cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)
                    self.update_velocities(x, y, z, x_ref, y_ref, z_ref)
                    self.change_new_state()

                else:
                    #print("no marker detected")
                    self.left_right, self.far_back, self.up_down, self.yaw = 0, 0, 0, 0
                    self.change_new_state()
            
            if (self.new_state != self.state):
                self.send_command_state = 1
        
        return frame