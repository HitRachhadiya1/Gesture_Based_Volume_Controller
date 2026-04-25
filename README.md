# AI-Based Gesture Recognition for System Control

## 🎯 Overview

A **touchless volume controller** powered by **Edge AI**. Uses your laptop's webcam to detect hand gestures in real-time and map a thumb–index finger pinch to the Windows system volume — no internet, no cloud, no extra hardware.

![demo](https://img.shields.io/badge/Platform-Windows-blue?style=flat-square) ![python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real-time hand tracking** | 21 landmark points detected per hand via MediaPipe |
| **Pinch-to-volume** | Euclidean distance between thumb & index finger controls volume |
| **Visual overlay** | Landmark dots, connecting line, volume bar, and FPS counter |
| **Edge processing** | Everything runs locally — zero latency from network calls |
| **Privacy-first** | No video data leaves your machine |

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **OpenCV** — webcam capture & GUI rendering
- **MediaPipe** — hand landmark detection (Google)
- **PyCaw** — Windows audio endpoint control
- **NumPy** — interpolation & math

---

## 📁 File Structure

```
gesture recognition project/
├── gesture_volume_controller.py   # Main application
├── hand_tracking_module.py        # Reusable HandDetector class
├── requirements.txt               # pip dependencies
├── README.md                      # This file
└── INSTALLATION_GUIDE.md          # Detailed setup instructions
```

---

## 🚀 Quick Start

```bash
# 1. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python gesture_volume_controller.py
```

> **Tip:** Pinch your thumb and index finger together to lower the volume; spread them apart to raise it. Press **q** to quit.

---

## 📚 References

- [MediaPipe Hands – Google](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV-Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PyCaw – GitHub](https://github.com/AndreMiras/pycaw)
