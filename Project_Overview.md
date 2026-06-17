# Head Tracking Missile Launcher: Project Overview

## 🛠️ Component List

1. **1x Arduino Nano** (The main microcontroller)
2. **2x Servo Motors** (e.g., SG90 or MG996R)
   - One for **Pan** (X-axis, sweeping left/right)
   - One for **Tilt** (Y-axis, aiming up/down)
3. **1x 5V Laser Module** (The targeting laser indicator)
4. **1x Laptop / PC with a Webcam** (To run the YOLOv8 AI)
5. **1x USB Cable** (To connect the Arduino Nano to your PC for Serial communication)
6. **Jumper Wires** (To connect the modules to the Nano)
7. *(Optional but Recommended)* **External 5V Power Supply**. Servos draw a lot of current when moving. If your Arduino Nano disconnects from the PC when the servos move, you need to power the servos from an external 5V source (Make sure to connect the external supply's GND to the Arduino's GND!).

---

## ⚙️ System Workflow

The system works in a continuous, high-speed loop between your laptop and the hardware:

1. **Vision (PC):** Your laptop's webcam captures a live video frame.
2. **AI Processing (PC):** The Python script passes the frame to the **YOLOv8 AI model**. The AI identifies the "person" in the frame and draws a bounding box around them.
3. **Targeting Math (PC):** The script mathematically calculates the top 20% of that bounding box to approximate where the person's **head** is.
4. **Correction Logic (PC):** It compares the head's position to the absolute center of the camera frame. 
   - If the head is to the left, it tells the Pan servo to decrease its angle.
   - If the head is too high, it tells the Tilt servo to adjust accordingly.
5. **Communication (PC ➔ Arduino):** Python formats these newly calculated X and Y angles into a simple text string (e.g., `"95,110\n"`) and sends it over the USB cable via Serial communication.
6. **Hardware Execution (Arduino):** The Arduino Nano receives the `"X,Y"` string, splits the two numbers, and commands the physical servos to move. As long as it is actively receiving data, it keeps the laser pin set to `HIGH` (ON).

---

## 🔌 Circuit Diagram

### ASCII Wiring Schematic
```text
                ┌──────────────────────┐
                │    ARDUINO NANO      │
                │                      │
                │ 5V  ─────────────┐   │
                │ GND ──────────┐  │   │
                │               │  │   │
                │ D9  ───────┐  │  │   │
                │ D10 ─────┐ │  │  │   │
                │ D11 ───┐ │ │  │  │   │
                └────────│─│─│──│──│───┘
                         │ │ │  │  │
         ┌───────────────┘ │ │  │  │
         │                 │ │  │  │
   ┌───────────┐     ┌───────────┐ │
   │ SERVO 1   │     │ SERVO 2   │ │
   │ (PAN)     │     │ (TILT)    │ │
   │ Signal → D9     │ Signal→D10│ │
   │ VCC    → 5V     │ VCC → 5V  │ │
   │ GND    → GND    │ GND → GND │ │
   └───────────┘     └───────────┘ │
                                   │
                             ┌──────────┐
                             │ LASER    │
                             │ S → D11  │
                             │ - → GND  │
                             │ + → 5V   │
                             └──────────┘
```

### Pin Summary
| Component | Arduino Pin | Wire Color (Typical) |
| :--- | :--- | :--- |
| **Servo 1 (Pan)** | `D9` | Signal: Orange/Yellow |
| **Servo 2 (Tilt)**| `D10` | Signal: Orange/Yellow |
| **Laser Signal** | `D11` | Signal: Varies |
| **All VCC (Power)**| `5V` | Red |
| **All GND (Ground)**| `GND` | Brown/Black |
