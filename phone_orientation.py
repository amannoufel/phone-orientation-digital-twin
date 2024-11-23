import websocket
import json
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import queue
import threading

class PhoneOrientationDigitalTwin:
    def __init__(self, accelerometer_url, magnetometer_url):
        self.accelerometer_url = accelerometer_url
        self.magnetometer_url = magnetometer_url
        self.data_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        # Store latest sensor readings
        self.accel_data = [0.0, 0.0, 0.0]
        self.mag_data = [0.0, 0.0, 0.0]
        
        # Matplotlib figure and axis as instance variables
        self.fig = None
        self.ax = None
    
    def calculate_orientation(self, ax, ay, az, mx, my, mz):
        # Roll (rotation around X)
        roll = math.atan2(float(ay), float(az)) * 180 / math.pi
        
        # Pitch (rotation around Y)
        pitch = math.atan2(-float(ax), math.sqrt(float(ay)*2 + float(az)*2)) * 180 / math.pi
        
        # Yaw (rotation around Z)
        # Tilt-compensated compass heading
        mx_comp = float(mx) * math.cos(math.radians(pitch)) + float(mz) * math.sin(math.radians(pitch))
        my_comp = float(mx) * math.sin(math.radians(roll)) * math.sin(math.radians(pitch)) + \
                  float(my) * math.cos(math.radians(roll)) - \
                  float(mz) * math.sin(math.radians(roll)) * math.cos(math.radians(pitch))
        
        yaw = math.atan2(-my_comp, mx_comp) * 180 / math.pi
        
        return roll, pitch, yaw
    
    def rotate_points(self, points, roll, pitch, yaw):
        # Convert degrees to radians
        roll_rad = math.radians(roll)
        pitch_rad = math.radians(pitch)
        yaw_rad = math.radians(yaw)
        
        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, math.cos(roll_rad), -math.sin(roll_rad)],
            [0, math.sin(roll_rad), math.cos(roll_rad)]
        ])
        
        Ry = np.array([
            [math.cos(pitch_rad), 0, math.sin(pitch_rad)],
            [0, 1, 0],
            [-math.sin(pitch_rad), 0, math.cos(pitch_rad)]
        ])
        
        Rz = np.array([
            [math.cos(yaw_rad), -math.sin(yaw_rad), 0],
            [math.sin(yaw_rad), math.cos(yaw_rad), 0],
            [0, 0, 1]
        ])
        
        # Apply rotations
        rotated_points = points @ Rx.T @ Ry.T @ Rz.T
        return rotated_points
    
    def create_phone_representation(self):
        return np.array([
            [0, 0, 0],    # Center
            [1, 0, 0],    # Length
            [-1, 0, 0],   # Negative Length
            [0, 2, 0],    # Width
            [0, -2, 0],   # Negative Width
            [0, 0, 0.5],  # Height
            [0, 0, -0.5]  # Negative Height
        ])
    
    def plot_thread(self):
        # Create figure and axis in the plotting thread
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        phone_body = self.create_phone_representation()
        
        while not self.stop_event.is_set():
            try:
                # Calculate orientation with latest data
                ax, ay, az = self.accel_data
                mx, my, mz = self.mag_data
                
                roll, pitch, yaw = self.calculate_orientation(ax, ay, az, mx, my, mz)
                
                self.ax.clear()
                self.ax.set_xlim([-3, 3])
                self.ax.set_ylim([-3, 3])
                self.ax.set_zlim([-3, 3])
                self.ax.set_xlabel('X')
                self.ax.set_ylabel('Y')
                self.ax.set_zlabel('Z')
                
                rotated_points = self.rotate_points(phone_body, roll, pitch, yaw)
                
                # Plot points and connections
                self.ax.scatter(rotated_points[:, 0], 
                           rotated_points[:, 1], 
                           rotated_points[:, 2], 
                           c='red', s=100)
                
                connections = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
                for start, end in connections:
                    self.ax.plot3D(
                        [rotated_points[start, 0], rotated_points[end, 0]],
                        [rotated_points[start, 1], rotated_points[end, 1]],
                        [rotated_points[start, 2], rotated_points[end, 2]], 
                        'blue', linewidth=3
                    )
                
                self.ax.set_title(f'Phone Orientation\nRoll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°')
                plt.draw()
                plt.pause(0.01)
            except Exception as e:
                print(f"Plotting error: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        plt.close()
    
    def on_accelerometer_message(self, ws, message):
        try:
            values = json.loads(message)['values']
            self.accel_data = [float(v) for v in values[:3]]
        except Exception as e:
            print(f"Accelerometer processing error: {e}")
    
    def on_magnetometer_message(self, ws, message):
        try:
            values = json.loads(message)['values']
            self.mag_data = [float(v) for v in values[:3]]
        except Exception as e:
            print(f"Magnetometer processing error: {e}")
    
    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")
    
    def on_close(self, ws, close_code, reason):
        print(f"Connection closed: {reason}")
        self.stop_event.set()
    
    def on_open(self, ws):
        print("WebSocket connection established")
    
    def connect(self):
        # Start plot thread first
        plot_thread = threading.Thread(target=self.plot_thread)
        plot_thread.start()
        
        # WebSocket for accelerometer
        accel_ws = websocket.WebSocketApp(
            self.accelerometer_url,
            on_open=self.on_open,
            on_message=self.on_accelerometer_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        # WebSocket for magnetometer
        mag_ws = websocket.WebSocketApp(
            self.magnetometer_url,
            on_open=self.on_open,
            on_message=self.on_magnetometer_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        # Run WebSocket connections
        accel_thread = threading.Thread(target=accel_ws.run_forever)
        mag_thread = threading.Thread(target=mag_ws.run_forever)
        
        accel_thread.start()
        mag_thread.start()
        
        # Wait for threads to complete
        accel_thread.join()
        mag_thread.join()

# Usage
digital_twin = PhoneOrientationDigitalTwin(
    "ws://10.37.194.39:8080/sensor/connect?type=android.sensor.accelerometer",
    "ws://10.37.194.39:8080/sensor/connect?type=android.sensor.magnetic_field"
)
digital_twin.connect()