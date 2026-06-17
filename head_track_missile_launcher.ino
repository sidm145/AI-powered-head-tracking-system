#include <Servo.h>

Servo servo1;
Servo servo2;
const int laserPin = 11;

int currentX = 90;
int currentY = 90;

void setup() {
  Serial.begin(9600);
  servo1.attach(9);
  servo2.attach(10);
  pinMode(laserPin, OUTPUT);
  
  // Center servos initially
  servo1.write(currentX);
  servo2.write(currentY);
  digitalWrite(laserPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    // Read string until newline: format "X,Y\n"
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    
    if (commaIndex > 0) {
      String xStr = data.substring(0, commaIndex);
      String yStr = data.substring(commaIndex + 1);
      
      currentX = xStr.toInt();
      currentY = yStr.toInt();
      
      servo1.write(currentX);
      servo2.write(currentY);
      
      // Keep laser ON while receiving commands
      digitalWrite(laserPin, HIGH);
    }
  } else {
    // Optional: Turn laser off if no connection for a long time
  }
}
