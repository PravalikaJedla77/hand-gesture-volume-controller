# 🖐️ Hand Gesture Volume Controller

A real-time computer vision application that controls the system volume using hand gestures.  
The project uses OpenCV and MediaPipe for hand tracking and Pycaw for system-level audio control.  
A YouTube video opens automatically to demonstrate live volume changes.

---

## 🚀 Features
- Real-time hand gesture detection
- Control system volume using thumb–index finger distance
- Automatic YouTube demo for clear audio feedback
- Live volume percentage display
- Easy to run and demo-friendly

---

## 🛠️ Tech Stack
- Python
- OpenCV
- MediaPipe
- Pycaw
- Comtypes

---

## ✅ Prerequisites
- Python 3.8 or higher
- Windows OS (required for Pycaw)
- Webcam

---

## ▶️ How to Run the Project

```bash
git clone https://github.com/PravalikaJedla77/hand-gesture-volume-controller.git
cd hand-gesture-volume-controller
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
