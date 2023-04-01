#include <Servo.h>
#include <PID_v1.h>

#define MAX_RPM 14400

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

double actual_speed0;
double actual_speed1;
double actual_speed2;

double setpiont_speed0 = 0;
double setpiont_speed1 = 0;
double setpiont_speed2 = 0;

double written_speed0 = 0;
double written_speed1 = 0;
double written_speed2 = 0;

Servo motor0;
Servo motor1;
Servo motor2;

double Kp=2, Ki=5, Kd=1;
PID motor0_PID(&actual_speed0, &written_speed0, &setpiont_speed0, Kp, Ki, Kd, DIRECT);
PID motor1_PID(&actual_speed1, &written_speed1, &setpiont_speed1, Kp, Ki, Kd, DIRECT);
PID motor2_PID(&actual_speed2, &written_speed2, &setpiont_speed2, Kp, Ki, Kd, DIRECT);
bool use_PID = true;

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
  digitalWrite(ledPin, HIGH);
  
  pinMode(motor0_interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motor0_interruptPin), tacho0, RISING);
  pinMode(motor1_interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motor1_interruptPin), tacho1, RISING);
  pinMode(motor2_interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motor2_interruptPin), tacho2, RISING);

  motor0.attach(motor0_pin);
  motor1.attach(motor1_pin);
  motor2.attach(motor2_pin);

  motor0_PID.SetMode(AUTOMATIC);
  motor1_PID.SetMode(AUTOMATIC);
  motor2_PID.SetMode(AUTOMATIC);
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
      setpiont_speed0 = 180;
      setpiont_speed1 = 180;
      setpiont_speed2 = 180;
    }
    if (data == 'u') {
      int tmp = Serial.parseInt();
      setpiont_speed0 = tmp;
      setpiont_speed1 = tmp;
      setpiont_speed2 = tmp;
      tmp = 0;
    }
    if (data == 'a') {
      setpiont_speed0 = Serial.parseInt();
    }
    if (data == 'b') {
      setpiont_speed1 = Serial.parseInt();
    }
    if (data == 'c') {
      setpiont_speed0 = Serial.parseInt();
    }
    if (data == 'p') {
      use_PID = true;
    }
    if (data == 'q') {
      use_PID = false;
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
  
  print_debug();
  
  if(use_PID){
    motor0_PID.Compute();
    motor1_PID.Compute();
    motor2_PID.Compute();
  }
  else{
    written_speed0 = setpiont_speed0;
    written_speed1 = setpiont_speed1;
    written_speed2 = setpiont_speed2;
  }
  motor0_writeRPM(written_speed0);
  motor1_writeRPM(written_speed1);
  motor2_writeRPM(written_speed2);
  
  delay(1);
}
