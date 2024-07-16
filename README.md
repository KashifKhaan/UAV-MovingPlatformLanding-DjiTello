# Autonomous Landing of UAV on Moving Platform Using Computer Vision

## Introduction
This project aims to develop a UAV system that can autonomously land on a moving platform using computer vision and control systems. The focus is on enhancing UAV technology by enabling drones to land on moving platforms with precision, which has applications in logistics, military, and rescue missions.

![image](https://github.com/user-attachments/assets/db815c15-0122-4b36-9e1c-5a8487fd339b)

## Table of Contents
- [Introduction](#introduction)
- [Screenshots and Videos](#screenshots-and-videos)
- [Background and Motivation](#background-and-motivation)
- [Objectives](#objectives)
- [Key Components](#key-components)
- [Camera Calibration](#camera-calibration)
- [Pose Estimation](#pose-estimation)
- [ArUco Markers](#aruco-markers)
- [PID Control System](#pid-control-system)
- [Workflow](#workflow)
- [Results](#results)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contributors](#contributors)

## Background and Motivation
Traditional UAV landing methods are limited and not suitable for dynamic environments. This project addresses this need for precision, with applications in logistics, military, and rescue missions.

## Screenshots and Videos
https://github.com/user-attachments/assets/efe6aa5e-7c5d-413b-8058-ab73d69cfaa0

https://github.com/user-attachments/assets/c310fbe9-0985-4bed-b44e-b981540e041b

## Objectives
1. Develop a vision-based system
2. Implement PID control
3. Ensure real-time data processing
4. Integrate systems
5. Conduct field testing

## Key Components
### Hardware Setup
- **DJI Tello Drone:** Chosen for its lightweight design, programmability, and onboard camera and sensors.

![image](https://github.com/user-attachments/assets/e8c3edd6-4240-4231-8001-6070c6beff81)

### Software Framework
- **Programming Language:** Python
- **IDE:** Visual Studio Code (VSCode)
- **Functions:** Real-time image processing and control algorithm implementation

### Control Interface Module
- **GUI Features:** Live feed from the camera, manual control buttons, autonomous landing buttons, feedback on altitude, temperature, and height.

![image](https://github.com/user-attachments/assets/24907fe4-583b-403c-9346-e89dc817098a)

## Camera Calibration
Camera calibration ensures accurate distance and angle measurements. This is crucial for determining the drone's position and orientation relative to the landing platform.

https://github.com/user-attachments/assets/c310fbe9-0985-4bed-b44e-b981540e041b

## Pose Estimation
Pose estimation determines the position and orientation of the drone relative to the landing platform. It uses the camera matrix and distortion coefficients obtained from camera calibration.

## ArUco Markers
ArUco markers are used for accurate pose estimation and object tracking. They are square-shaped patterns with a unique identifier, high detectability, and are easy to use.

![image](https://github.com/user-attachments/assets/c56e2989-6e93-4d30-8c61-3a642d3d46ac)

### Advantages of Using ArUco Markers
- **Ease of Use:** Easy to print and deploy.
- **Open-Source Libraries:** Available libraries like OpenCV's ArUco module simplify development.
- **Accuracy:** Provide reliable pose estimation essential for precise UAV landings.

### Limitations
- **Lighting Conditions:** Detection accuracy can be affected by extreme lighting.
- **Distance and Size:** Detection range is limited by camera resolution and marker size.

## PID Control System
The PID control system is a feedback control mechanism that includes Proportional, Integral, and Derivative components. It is essential for real-time adjustments and precise landings.

### Role in UAV Control
- **Maintain Stability:** Continuous adjustments to UAV's flight parameters.
- **Track the Moving Platform:** Adjusts flight path based on pose information from the vision system.
- **Achieve Precision Landings:** Fine-tuning of PID parameters for precise and smooth landings.

## Workflow
1. **Initialization**
2. **Data Reception and Processing**
3. **Decision Execution**
4. **Feedback Analysis**

## Results
The system was tested in an indoor environment using the DJI Tello UAV, showing an excellent level of accuracy and precision.

## Limitations
- **Computational Power:** Insufficient for real-time processing.
- **Data Transmission:** Latency between the UAV and ground station.

## Future Work
- **Algorithm Optimization:** Improve computational efficiency.
- **Alternative Sensors:** Explore LIDAR or infrared sensors.
- **AI Integration:** Incorporate machine learning and deep learning for increased autonomy and flexibility.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/autonomous-uav-landing.git
    ```
2. Navigate to the project directory:
    ```bash
    cd autonomous-uav-landing
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Ensure the DJI Tello Drone is powered on and connected to your Wi-Fi network.
2. Run the main script to start the autonomous landing system:
    ```bash
    python main.py
    ```
3. Use the GUI to monitor the live feed and control the UAV.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors
- Mohammad Kashif
- Nabeel Ahmad
- Muneer Ahmad
