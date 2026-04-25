# Installation Guide — AI-Based Gesture Recognition

Follow these steps **in order** to set up and run the project on Windows.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 10 / 11 |
| **Python** | 3.8 – 3.11 (3.12 works but MediaPipe may lag behind) |
| **Webcam** | Built-in or external USB camera |
| **RAM** | 4 GB minimum |

---

## Step 1 — Install Python

If Python is not already installed:

1. Download the installer from **[python.org/downloads](https://www.python.org/downloads/)**.
2. **Check the box** _"Add Python to PATH"_ during installation.
3. Verify:
   ```bash
   python --version
   ```
   You should see something like `Python 3.11.x`.

---

## Step 2 — Open a Terminal in the Project Folder

Open **Command Prompt** or **PowerShell**, then navigate to the project:

```bash
cd "E:\gesture recognition project"
```

---

## Step 3 — Create a Virtual Environment (recommended)

```bash
python -m venv venv
```

Activate it:

```bash
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

> Your prompt should now start with `(venv)`.

---

## Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
| Package | Purpose |
|---------|---------|
| `opencv-python` | Webcam capture & image display |
| `mediapipe` | Hand landmark detection (21 points) |
| `pycaw` | Windows audio volume control |
| `numpy` | Math / interpolation |
| `comtypes` | COM interface (required by PyCaw) |

---

## Step 5 — Run the Application

```bash
python gesture_volume_controller.py
```

A window titled **"AI Gesture Volume Controller"** will open showing your webcam feed.

### How to use

1. Hold your hand in front of the webcam.
2. **Pinch** your thumb and index finger together → volume **decreases**.
3. **Spread** them apart → volume **increases**.
4. Press **`q`** to quit.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Make sure the virtual environment is activated and you ran `pip install -r requirements.txt` |
| Camera not opening | Check that no other app (Zoom, Teams) is using the webcam |
| `pycaw` errors | PyCaw is **Windows-only**. It will not work on macOS/Linux |
| Low FPS | Close other heavy applications; ensure no other process is using the camera |
| MediaPipe install fails on Python 3.12+ | Use Python 3.11 instead: `py -3.11 -m venv venv` |

---

## Uninstall / Clean Up

```bash
deactivate           # exit the virtual environment
rmdir /s /q venv     # delete the virtual environment folder
```

---

_Happy gesture controlling! 🖐️_
