import customtkinter
import cv2
from PIL import Image, ImageTk

class gui(customtkinter.CTk):
    def __init__(self, window_size = "800x600", video_size = (600, 400), track_obj = None):
        super().__init__()
        self.track_obj = track_obj
        self.title("Mission Control")
        self.geometry(window_size)
        self.video_size = video_size

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.x, self.y, self.dx, self.dy = 0.1, 0.75, 0.2, 0.2

        self.left_button = self.create_button("LEFT", self.x + 0.05 , self.y + self.dy/2, self.button_pressed, self.button_released)
        self.right_button = self.create_button("RIGHT", self.x + 2*self.dx - 0.05, self.y + self.dy/2, self.button_pressed, self.button_released)
        self.far_button = self.create_button("FORWARD", self.x + self.dx, self.y, self.button_pressed, self.button_released)
        self.back_button = self.create_button("BACKWARD", self.x + self.dx, self.y + self.dy, self.button_pressed, self.button_released)
        self.up_button = self.create_button("UP", self.x + 2.8*self.dx , self.y, self.button_pressed, self.button_released)
        self.down_button = self.create_button("DOWN", self.x + 2.8*self.dx, self.y + self.dy, self.button_pressed, self.button_released)

        self.down_button = self.create_button("TRACKANDLAND", self.x + 3.8*self.dx, self.y, self.button_pressed, self.button_released)
        self.down_button = self.create_button("LAND", self.x + 3.8*self.dx, self.y + self.dy, self.button_pressed, self.button_released)

        self.video_frame = customtkinter.CTkFrame(self, width=self.video_size[0], height=self.video_size[1],
                                                  border_width=6, border_color="white")
        self.video_frame.pack(side="left", padx = 50, pady = 20, anchor = "n")
        
        self.video_label = customtkinter.CTkLabel(self.video_frame, width=self.video_size[0], height=self.video_size[1], text = "")
        self.video_label.pack(padx=4, pady=4)
        self.video_label.pack(fill=customtkinter.BOTH, expand=True)

        self.info_frame = customtkinter.CTkFrame(self, width=400, height=100, border_width=0, fg_color="transparent")
        self.info_frame.pack(side="left", padx = 10, pady = 130, anchor = "n")

        # Create labels for real-time information
        self.battery_label = customtkinter.CTkLabel(self.info_frame, width=250, text=f"Battery : NA %", 
                                                    text_color="yellow", font=("Arial", 20), anchor="w")
        self.battery_label.pack(side="top", padx=20, pady=30)
        self.temperature_label = customtkinter.CTkLabel(self.info_frame, width=250, text=f"Temperature: °C",
                                                        text_color="yellow", font=("Arial", 20), anchor="w")
        self.temperature_label.pack(side="top", padx=20, pady=30)
        self.altitude_label = customtkinter.CTkLabel(self.info_frame, width=250, text=f"Altitude: cm",
                                                     text_color="yellow", font=("Arial", 20), anchor="w")
        self.altitude_label.pack(side="top", padx=20, pady=30)
        #self.speed_label = customtkinter.CTkLabel(self.info_frame, width=200, text=f"Speed:  m/s",
        #                                          text_color="yellow", font=("Arial", 20), anchor="w")
        #self.speed_label.pack(side="top", padx=20, pady=20)

    def create_button(self, text, rel_x, rel_y, func1, func2):
        button = customtkinter.CTkButton(self, text=text,
                                         fg_color=("blue", "black"),
                                         width=100, height=50, border_width=3, 
                                         corner_radius=20)
        button.place(relx = rel_x, rely = rel_y, anchor=customtkinter.CENTER)
        button.bind("<Button-1>", lambda event, button_text=text: func1(event, button_text))
        button.bind("<ButtonRelease-1>", lambda event, button_text=text: func2(event, button_text))
        return button
    

    def button_pressed(self, event, button_text):
        self.track_obj.button_check = 1
        self.track_obj.left_right, self.track_obj.far_back = 0, 0
        self.track_obj.up_down, self.track_obj.yaw = 0, 0
        speed = 40
        if button_text == "LEFT":
            self.track_obj.left_right = -speed
            self.track_obj.change_new_state()
        elif button_text == "RIGHT":
            self.track_obj.left_right = speed
            self.track_obj.change_new_state()
        elif button_text == "FORWARD":
            self.track_obj.far_back = speed
            self.track_obj.change_new_state()
        elif button_text == "BACKWARD":
            self.track_obj.far_back = -speed
            self.track_obj.change_new_state()
        elif button_text == "UP":
            self.track_obj.up_down = speed
            self.track_obj.change_new_state()
        elif button_text == "DOWN":
            self.track_obj.up_down= -speed
            self.track_obj.change_new_state()
        elif button_text == "LAND":
            if self.track_obj.land_state == 0:
                self.track_obj.land_state = 1
        elif button_text == "TRACKANDLAND":
            self.track_obj.trackandland = 1
    
    def button_released(self, event, button_text):
        if button_text == "LAND":
            pass
        else:
            self.track_obj.left_right, self.track_obj.far_back = 0, 0
            self.track_obj.up_down, self.track_obj.yaw = 0, 0, 
            self.track_obj.change_new_state()
            self.track_obj.button_check = 0
    
    def update_video(self, img):
        # Convert the image from BGR color (which OpenCV uses) to RGB color
        #rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Convert the image to PIL format
        pil_image = Image.fromarray(img)
        # Convert the PIL image to CTkImage
        tk_image = customtkinter.CTkImage(dark_image=pil_image, size = (self.video_size[0], self.video_size[1]))
        # Update the label with the new image
        self.video_label.configure(image=tk_image)
        self.video_label.image = tk_image
