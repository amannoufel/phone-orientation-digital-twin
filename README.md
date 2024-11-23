# Phone Orientation Digital Twin 📱

A real-time 3D visualization system that creates a digital twin of a phone's orientation using accelerometer and magnetometer sensor data. The system processes sensor data through WebSocket connections and displays a live 3D representation of the phone's orientation using matplotlib.


## 🚀 Features

- Real-time 3D visualization of phone orientation
- WebSocket connection to phone sensors
- Processing of accelerometer and magnetometer data
- Calculation of roll, pitch, and yaw angles
- Multi-threaded design for smooth performance
- Live updating 3D plot using matplotlib

## 📋 Prerequisites

- Python 3.x
- Required packages:
  ```bash
  pip install websocket-client
  pip install numpy
  pip install matplotlib
  ```

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/phone-orientation-digital-twin.git
   cd phone-orientation-digital-twin
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Update the WebSocket URLs in the main script to match your phone's IP address and port:
   ```python
   digital_twin = PhoneOrientationDigitalTwin(
       "ws://YOUR_PHONE_IP:8080/sensor/connect?type=android.sensor.accelerometer",
       "ws://YOUR_PHONE_IP:8080/sensor/connect?type=android.sensor.magnetic_field"
   )
   ```

2. Run the script:
   ```bash
   python phone_orientation.py
   ```

## 🔧 How It Works

The system consists of several key components:

1. **WebSocket Connections**: Establishes connections to phone sensors to receive real-time data
2. **Orientation Calculation**: Processes accelerometer and magnetometer data to determine phone orientation
3. **3D Visualization**: Creates a real-time 3D representation of the phone using matplotlib
4. **Multi-threading**: Handles data collection and visualization in separate threads for smooth performance

## 📁 Project Structure

```
phone-orientation-digital-twin/
├── phone_orientation.py    # Main application file
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Your Name - [@YourTwitterHandle](https://twitter.com/YourTwitterHandle)

Project Link: [https://github.com/YOUR_USERNAME/phone-orientation-digital-twin](https://github.com/YOUR_USERNAME/phone-orientation-digital-twin)

## 🙏 Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc

## 📞 Contact

Your Name - [@YourTwitterHandle](https://twitter.com/YourTwitterHandle)

Email - your.email@example.com