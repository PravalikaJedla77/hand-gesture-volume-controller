<!-- README updated -->
# ✋ Hand Gesture Volume Controller using Python

This project uses computer vision and hand tracking to control your system volume with simple hand gestures.

## 📸 Demo
Real-time volume control by measuring distance between thumb and index finger!

## 🔧 Technologies Used

- Python
- OpenCV
- MediaPipe
- Pycaw (for system audio control)

## 🖥️ How It Works

- Detects hand landmarks using MediaPipe
- Measures distance between thumb tip and index tip
- Maps distance to system volume
- Displays volume % and interactive volume bar

## 📦 Installation

```bash
pip install opencv-python mediapipe pycaw comtypes
