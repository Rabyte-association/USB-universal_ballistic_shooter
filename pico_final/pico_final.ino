#include <Servo.h>

const byte ledPin = 25;

const byte motor0_interruptPin = 16;
const byte motor1_interruptPin = 18;
const byte motor2_interruptPin = 20;

const byte motor0_pin = 17;
const byte motor1_pin = 19;
const byte motor2_pin = 21;

float current_time = 0;
float prev_time = 0;
float delta_t_s = 0;
float counter0 = 0;
float counter1 = 0;
float counter2 = 0;

int actual_speed0;
int actual_speed1;
int actual_speed2;

int desired_speed0 = 0;
int desired_speed1 = 0;
int desired_speed2 = 0;

int written_speed0 = 0;
int written_speed1 = 0;
int written_speed2 = 0;

Servo motor0;
Servo motor1;
Servo motor2;

void tacho0() {
  counter0 += 1;
}
void tacho1() {
  counter1 += 1;
}
void tacho2() {
  counter2 += 1;
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  pinMode(motor0_interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motor0_interruptPin), tacho0, RISING);
  pinMode(motor1_interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motor1_interruptPin), tacho1, RISING);
  pinMode(motor2_interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motor2_interruptPin), tacho2, RISING);

  motor0.attach(motor0_pin);
  motor1.attach(motor1_pin);
  motor2.attach(motor2_pin);
}

void loop() {
  if (Serial.available() > 1) {
    byte data = Serial.read();
    if (data == 's') {
      written_speed0 = 0;
      written_speed1 = 0;
      written_speed2 = 0;
    }
    if (data == 'f') {
      desired_speed0 = 180;
      desired_speed1 = 180;
      desired_speed2 = 180;
    }
    if (data == 'u') {
      int tmp = Serial.parseInt();
      desired_speed0 = tmp;
      desired_speed1 = tmp;
      desired_speed2 = tmp;
      tmp = 0;
    }
    if (data == 'a') {
      desired_speed0 = Serial.parseInt();
    }
    if (data == 'b') {
      desired_speed1 = Serial.parseInt();
    }
    if (data == 'c') {
      desired_speed0 = Serial.parseInt();
    }
  }
  current_time = millis();
  delta_t_s = (current_time - prev_time) / 1000;
  actual_speed0 = (counter0 / delta_t_s) * 60;
  actual_speed1 = (counter1 / delta_t_s) * 60;
  actual_speed2 = (counter2 / delta_t_s) * 60;
  counter0 = 0;
  counter1 = 0;
  counter2 = 0;
  prev_time = current_time;
  Serial.print(actual_speed0);
  Serial.print(", ");
  Serial.print(actual_speed1);
  Serial.print(", ");
  Serial.println(actual_speed2);

  Serial.print(desired_speed0);
  Serial.print(", ");
  Serial.print(desired_speed1);
  Serial.print(", ");
  Serial.println(desired_speed2);

  motor0.write(desired_speed0);
  motor1.write(desired_speed1);
  motor2.write(desired_speed2);
  delay(1);
}
