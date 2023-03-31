#include <Servo.h>
int speed1 = 0;
int speed2 = 0;
int speed3 = 0;
int speed4 = 0;

int tmp = 0;
bool stoper = false;
Servo top;
Servo left;
Servo right;
Servo fan;
// The setup routine runs once when you press reset.
void setup() {
  Serial.begin(115200);
  top.attach(17);
  left.attach(19);
  right.attach(21);
  fan.attach(0);

}


// The loop routine runs over and over again forever.
void loop() {
if (Serial.available() > 1) {
  byte data = Serial.read();
    if (data == 's'){
      speed1=0;
      speed2=0;
      speed3=0;
      speed4=0;
    }
    if (data == 'f'){
      speed1=180;
      speed2=180;
      speed3=180;
    }
    if (data == 'u') {
      tmp = Serial.parseInt();
      speed1=tmp;
      speed2=tmp;
      speed3=tmp;
      tmp=0;
    }
    if (data == 'a') {
      speed1 = Serial.parseInt();
    }
    if (data == 'b') {
      speed2 = Serial.parseInt();
    }
    if (data == 'c') {
      speed3 = Serial.parseInt();
    }
    if (data == 'w') {
      speed4 = Serial.parseInt();
    }
    
    Serial.println(speed1);
    Serial.println(speed2);
    Serial.println(speed3);
    Serial.println(speed4);

}

      top.write(speed1);
      left.write(speed2);
      right.write(speed3); 
      fan.write(speed4);

}
