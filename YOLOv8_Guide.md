# 🎯 YOLOv8 Head Tracking Missile Launcher Guide

This guide will help you connect your Arduino Nano to a Python script that uses your laptop camera and **YOLOv8** to track a person's head and aim a laser/servo mechanism.

---

## 🛠️ Step 1: Install Python
1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer.
3. ⚠️ **CRITICAL:** At the bottom of the first installation screen, check the box **"Add Python to PATH"**.
4. Click **"Install Now"**.

---

## 🔍 Step 2: Verify Installation
1. Press `Win + R`, type `cmd` and hit **Enter**.
2. Type: 
   ```bash
   python --version
   ```
   *You should see your Python version printed (e.g., Python 3.12).*
3. Type:
   ```bash
   pip --version
   ```
   *This ensures the Python package manager is installed.*

---

## 📁 Step 3: Setup Project Directory
1. Open CMD (Command Prompt).
2. Navigate to your project folder on your Desktop:
   ```bash
   cd Desktop\"head trach missil lancher"
   ```
3. **Create a Virtual Environment** (Highly Recommended to keep things clean):
   ```bash
   python -m venv venv
   ```
4. **Activate the Virtual Environment**:
   ```bash
   venv\Scripts\activate
   ```
   *Note: Your command prompt should now say `(venv)` at the beginning.*

---

## 📦 Step 4: Install Required Libraries
With your virtual environment activated `(venv)`, run the following command to install the AI and camera libraries:

```bash
pip install ultralytics opencv-python pyserial
```
*Wait for the installation to finish. This downloads **YOLOv8** (`ultralytics`), your webcam library (`opencv`), and the Arduino communicator (`pyserial`).*

---

## ⚡ Step 5: Flash the Arduino Code
1. I have already updated `head_track_missile_launcher.ino` for you in this folder.
2. Open it in the **Arduino IDE**.
3. Select your **Arduino Nano** and the correct **COM Port** in the Tools menu.
4. Click **Upload**.
5. 📝 **Note down the COM Port number** (e.g., `COM3`).
6. **IMPORTANT:** Close the Arduino IDE Serial Monitor if it's open (it will block Python from connecting).

---

## 🚀 Step 6: Configure and Run the Tracker
1. Open the `tracker.py` file in a text editor (Notepad, VS Code, or right here in the IDE).
2. Look at **Line 8**: 
   ```python
   COM_PORT = 'COM3' 
   ```
3. Change `'COM3'` to whatever your Arduino Nano's port is.
4. Save the file.
5. In your CMD (with `venv` activated), run the tracker:
   ```bash
   python tracker.py
   ```

### 🎉 What Happens Next?
- When you run it the first time, YOLOv8 will automatically download `yolov8n.pt` (a small AI weights file).
- Your webcam will turn on, and a window will pop up showing the tracking.
- The script calculates your head position and sends the coordinates directly to the Arduino Nano servos!

To quit the camera tracking, click on the camera window and press `q`.
