#include <Servo.h>
int speed1 = 0;
int speed2 = 0;
int speed3 = 0;
int speed4 = 0;
int closedtop = 125;
int openedtop=100;
int closedbottom=160;
int openedbottom=100;


int tmp = 0;
bool stoper = false;
Servo top;
Servo left;
Servo right;
Servo fan;
Servo feedtop;
Servo feedbot;
// The setup routine runs once when you press reset.
void setup() {
  Serial.begin(115200);
  top.attach(17);
  left.attach(19);
  right.attach(21);
  fan.attach(1);
  feedbot.attach(3);
  feedtop.attach(2);
  feedtop.write(125);
  feedbot.write(180);
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
    else if (data == 'a') {
      speed1 = Serial.parseInt();
    }
    else if (data == 'b') {
      speed2 = Serial.parseInt();
    }
    else if (data == 'c') {
      speed3 = Serial.parseInt();
    }
    else if (data == 'w') {
      speed4 = Serial.parseInt();
    }
    else if (data == 't') {
      feedtop.write(openedtop);
      delay(200);
      feedtop.write(closedtop);
    }
    else if(data=='y'){
      feedbot.write(openedbottom);
      delay(250);
      feedbot.write(closedbottom);
    }
    else if(data=='l'){
    feedtop.write(openedtop);
    feedbot.write(openedbottom);
    delay(500);
    feedtop.write(closedtop);
    feedbot.write(closedbottom);
    Serial.println("tu");

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