# 🚗 Smart Parking Slot Detection System

An IoT-based intelligent parking management system that uses computer vision and ESP32-CAM to detect parking slot availability in real-time. Features a web-based dashboard for monitoring, live video feed processing, and automated slot status updates.

![Smart Parking Dashboard](images/slot.jpeg)

## 🌟 Overview

This project addresses the common problem of finding available parking spaces by automating the detection process using computer vision techniques. The system monitors a parking lot through a camera feed, processes the video in real-time, and displays the availability status of each parking slot on an intuitive web interface.

## ✨ Key Features

### 📹 Real-Time Detection
- **Live Video Processing**: Continuous monitoring of parking lot via ESP32-CAM
- **Computer Vision**: OpenCV-based slot detection using adaptive thresholding
- **Instant Updates**: Real-time status updates (Free/Parked)
- **69 Parking Slots**: Simultaneous monitoring of multiple parking spaces

### 🎛️ Interactive Dashboard
- **Slot Availability Display**: Visual grid showing all 69 parking slots
- **Color-Coded Status**: 
  - 🟢 Green = Free slot
  - 🔴 Red = Occupied slot
- **Live Statistics**: Real-time count of available parking slots (e.g., 15/69)
- **Video Feed**: Live parking lot camera view with bounding boxes
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### ⚙️ Adjustable Parameters
- **Adaptive Threshold Block Size**: Fine-tune detection sensitivity
- **Adaptive Threshold C**: Adjust detection accuracy
- **Median Blur Kernel**: Configure noise reduction
- **Video Upload**: Test with pre-recorded parking lot videos

### 🔌 Hardware Integration
- **ESP32-CAM**: Low-cost camera module for video streaming
- **Arduino**: Microcontroller for sensor integration
- **LCD Display**: Shows slot information locally
- **Sensors**: IR/Ultrasonic sensors for additional detection
- **Wi-Fi Connectivity**: Wireless communication and web hosting

## 🛠️ Technology Stack

### Hardware
- **ESP32-CAM** - Video streaming and Wi-Fi communication
- **Arduino UNO/Nano** - Sensor data processing
- **LCD Display (16x2)** - Local information display
- **IR/Ultrasonic Sensors** - Backup detection mechanism
- **Jumper Wires & Breadboard** - Circuit connections
- **Power Supply** - 5V power source

### Software
- **Python 3.x** - Backend processing
- **OpenCV** - Computer vision and image processing
- **Flask/Streamlit** - Web framework for dashboard
- **NumPy** - Numerical computations
- **cvzone** - Computer vision utilities
- **Pickle** - Data serialization for slot positions
- **Arduino IDE** - ESP32-CAM programming

### Computer Vision Techniques
- Adaptive Thresholding
- Median Blur filtering
- Contour detection
- Color space conversion (BGR to Grayscale)
- Region of Interest (ROI) analysis

## 📸 Screenshots

### Dashboard Interface
![Dashboard](images/slot.jpeg)

### Hardware Setup
![Hardware Setup](images/hardware.jpeg)

### Live Detection
![Live Detection](images/live.jpeg)

### **Prerequisites**
```bash
# Python 3.8 or higher
python --version

# Required libraries
pip install opencv-python
pip install numpy
pip install flask
pip install cvzone
pip install streamlit
```

### **Hardware Setup**

1. **ESP32-CAM Connection**
```
   ESP32-CAM → FTDI Programmer
   - GND → GND
   - 5V → 5V
   - U0R → TX
   - U0T → RX
   - GPIO 0 → GND (for programming mode)
```

2. **Arduino Connections**
```
   Arduino → LCD Display (I2C)
   - SDA → A4
   - SCL → A5
   - VCC → 5V
   - GND → GND
```

3. **Sensor Connections** (Optional)
```
   IR Sensor → Arduino
   - VCC → 5V
   - GND → GND
   - OUT → Digital Pin 2-13
```

### **Software Installation**
```bash
# 1. Clone the repository
git clone https://github.com/sasit622/Smart-Parking-Detection.git
cd Smart-Parking-Detection

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Upload ESP32-CAM code
# Open Arduino IDE
# Load esp32cam_code.ino
# Select Board: AI Thinker ESP32-CAM
# Upload code

# 4. Configure network settings
# Edit config.py with your ESP32-CAM IP address
ESP32_IP = "192.168.4.1"  # Replace with actual IP

# 5. Run the application
python app.py
# or
streamlit run dashboard.py
```


## 🎯 How It Works

### **Detection Algorithm**

1. **Video Capture**
```python
   # Capture frame from ESP32-CAM or video file
   cap = cv2.VideoCapture(video_source)
   ret, frame = cap.read()
```

2. **Preprocessing**
```python
   # Convert to grayscale
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
   # Apply median blur to reduce noise
   blur = cv2.medianBlur(gray, median_kernel)
   
   # Adaptive thresholding
   thresh = cv2.adaptiveThreshold(
       blur, 255, 
       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
       cv2.THRESH_BINARY_INV,
       block_size, threshold_c
   )
```

3. **Slot Analysis**
```python
   # For each parking slot
   for slot in parking_slots:
       # Extract ROI (Region of Interest)
       roi = thresh[y:y+h, x:x+w]
       
       # Count white pixels
       white_pixels = cv2.countNonZero(roi)
       
       # Determine status
       if white_pixels > threshold:
           status = "Occupied"
       else:
           status = "Free"
```

4. **Display Results**
   - Draw bounding boxes on frame
   - Update slot status in dashboard
   - Calculate free/total slots
   - Stream to web interface

### **System Architecture**
```
┌─────────────────┐
│   ESP32-CAM     │ ──► Video Stream
│  (Parking Lot)  │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│  OpenCV         │ ──► Image Processing
│  Processing     │     - Grayscale conversion
└─────────────────┘     - Noise reduction
        │               - Thresholding
        ▼
┌─────────────────┐
│  Detection      │ ──► Slot Analysis
│  Algorithm      │     - ROI extraction
└─────────────────┘     - Pixel counting
        │               - Status determination
        ▼
┌─────────────────┐
│  Web Dashboard  │ ──► Display
│  (Flask/Stream) │     - Slot grid
└─────────────────┘     - Statistics
                        - Live feed
```

## 🎨 Dashboard Features

### **Navigation Menu**
- 🧭 **Navigation**: Switch between different views
- 🅿️ **Slot Availability**: View real-time slot status
- 📹 **Live Detection**: Watch live camera feed with detections

### **Parameters Panel**
Adjust detection settings in real-time:
- **Adaptive Threshold Block Size**: 1-99 (default: 25)
- **Adaptive Threshold C**: 1-50 (default: 16)
- **Median Blur Kernel**: 1-15 (default: 5)

### **Video Upload**
- Upload custom parking lot videos for testing
- Supports MP4, AVI, MOV formats
- Maximum file size: 200MB
- Real-time processing of uploaded videos

### **Slot Status Grid**
- 69 parking slots displayed in organized grid
- Color-coded visual representation
- Individual slot numbers (Slot 1 - Slot 69)
- Click-to-highlight functionality (optional)

## 📊 Performance Metrics

- **Detection Accuracy**: ~92-95% under good lighting
- **Processing Speed**: 15-25 FPS on standard PC
- **Response Time**: <100ms for status update
- **False Positives**: <5% with optimal parameters
- **Wi-Fi Range**: Up to 50 meters (ESP32-CAM)

## 🔧 Configuration

### **Parking Slot Definition**

To define parking slots, run the slot selector:
```python
python slot_selector.py

# Instructions:
# 1. Click to mark first corner of parking slot
# 2. Click to mark opposite corner
# 3. Press 's' to save
# 4. Press 'r' to remove last slot
# 5. Press 'q' to quit
```

Slots are saved in `parking_slots.pkl`

### **ESP32-CAM Configuration**
```cpp
// WiFi credentials
const char* ssid = "YourWiFiSSID";
const char* password = "YourPassword";

// Camera settings
#define CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
```

### **Detection Parameters**

Optimal values (adjust based on your environment):
```python
BLOCK_SIZE = 25        # Adaptive threshold block size
THRESHOLD_C = 16       # Adaptive threshold constant
MEDIAN_KERNEL = 5      # Blur kernel size
MIN_PIXEL_THRESHOLD = 900  # Minimum pixels for "occupied"
```

## 🚦 Use Cases

- **Shopping Malls**: Guide customers to available parking
- **Airports**: Manage large parking facilities
- **Corporate Event**: Concerts.... 

## 🔮 Future Enhancements

- [ ] License plate recognition (LPR/ANPR)
- [ ] Mobile app (Android/iOS)
- [ ] Payment integration for paid parking
- [ ] Historical data analytics and reporting
- [ ] AI-based predictive parking availability
- [ ] Multi-camera support for larger lots
- [ ] Cloud storage for video footage
- [ ] Email/SMS notifications for users
- [ ] Reserved parking slot management
- [ ] Integration with Google Maps/Navigation apps
- [ ] Night vision support with IR LEDs
- [ ] Weather-resistant outdoor housing

## 🐛 Troubleshooting

### **Common Issues**

**ESP32-CAM won't connect:**
- Check WiFi credentials
- Verify power supply (min 5V 2A)
- Reset ESP32-CAM and reconnect
- Check IP address configuration

**Poor detection accuracy:**
- Adjust lighting conditions
- Tune adaptive threshold parameters
- Clean camera lens
- Redefine parking slot positions

**Low FPS/Lag:**
- Reduce video resolution
- Optimize code for better performance
- Use more powerful processing unit
- Reduce number of slots being monitored

**Video feed not showing:**
- Check ESP32-CAM IP address
- Verify network connectivity
- Restart Flask/Streamlit server
- Check firewall settings

## 📚 Learning Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [ESP32-CAM Getting Started](https://randomnerdtutorials.com/esp32-cam-video-streaming-face-recognition-arduino-ide/)
- [Computer Vision Basics](https://www.pyimagesearch.com/)
- [Arduino Reference](https://www.arduino.cc/reference/en/)

