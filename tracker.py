import cv2
from ultralytics import YOLO
import serial
import time

# ==========================================
# 1. SETUP ARDUINO SERIAL CONNECTION
# ==========================================
# IMPORTANT: Replace 'COM3' with your actual Arduino COM Port (e.g., COM4, COM5)
COM_PORT = 'COM3' 
BAUD_RATE = 9600

try:
    print(f"Connecting to Arduino on {COM_PORT}...")
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Give Arduino time to reset after serial connection
    print("Successfully connected to Arduino!")
except Exception as e:
    print(f"ERROR: Could not connect to Arduino: {e}")
    print("Running in Test Mode (No Serial output).")
    arduino = None

# ==========================================
# 2. LOAD YOLOv8 MODEL
# ==========================================
print("Loading YOLOv8 model... (This may download the model on first run)")
model = YOLO('yolov8n.pt')

# ==========================================
# 3. INITIALIZE WEBCAM
# ==========================================
print("Opening Web Camera...")
cap = cv2.VideoCapture(0)

# Camera Resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

center_x = 640 // 2
center_y = 480 // 2

# Initial Servo Angles (Centered)
servo_x = 90
servo_y = 90

print("Starting tracking loop. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from camera. Exiting...")
        break

    # Run YOLOv8 on the frame (looking only for class 0 -> 'person')
    results = model(frame, classes=[0], verbose=False)

    best_box = None
    max_area = 0

    # Find the largest person in the frame (closest to camera)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            area = (x2 - x1) * (y2 - y1)
            if area > max_area:
                max_area = area
                best_box = (x1, y1, x2, y2)

    if best_box:
        x1, y1, x2, y2 = best_box
        
        # Estimate head position (Top 20% of the person's bounding box)
        head_x = x1 + (x2 - x1) // 2
        head_y = y1 + (y2 - y1) // 5
        
        # Draw bounding boxes and targets
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)       # Blue box for person
        cv2.circle(frame, (head_x, head_y), 8, (0, 0, 255), -1)        # Red dot for head target
        cv2.putText(frame, "TARGET LOCKED", (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Map position to servo movements
        # Adjust speeds based on how far the target is from the center
        error_x = head_x - center_x
        error_y = head_y - center_y
        
        # Pan (Left/Right)
        if error_x < -30:
            servo_x += 2 # Move Right
        elif error_x > 30:
            servo_x -= 2 # Move Left
            
        # Tilt (Up/Down) - Note: Image Y goes down, Servo Y mapping depends on hardware mounting
        if error_y < -30:
            servo_y -= 2 # Move Up
        elif error_y > 30:
            servo_y += 2 # Move Down

        # Clamp angles to valid servo range (0 to 180 degrees)
        servo_x = max(0, min(180, servo_x))
        servo_y = max(0, min(180, servo_y))

        # Send target coordinates to Arduino via Serial
        if arduino:
            command = f"{servo_x},{servo_y}\n"
            arduino.write(command.encode('utf-8'))
            
        # Display Current Angle Info
        cv2.putText(frame, f"Pan(X): {servo_x}  Tilt(Y): {servo_y}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Draw Center Crosshair
    cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), (0, 255, 0), 2)
    cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), (0, 255, 0), 2)

    cv2.imshow('YOLOv8 Head Tracking Missile Launcher', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
print("Cleaning up...")
cap.release()
cv2.destroyAllWindows()
if arduino:
    # Reset servos to center before closing
    arduino.write("90,90\n".encode('utf-8'))
    time.sleep(1)
    arduino.close()
