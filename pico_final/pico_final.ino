// software for controling the universal balistic shooter
// using standard esc, hall sensors as tachometers and pid controller
// runs on rpi pico, using the arduino core by Earle F. Philhower is recomended
// by Team Rabyte 2023

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
const byte servoTop_pin = 2;
const byte servoBot_pin = 3;
const byte fan_pin = 3;

const byte closedtop = 125;
const byte openedtop=100;
const byte closedbottom=160;
const byte openedbottom=100;

float current_time = 0;
float prev_time = 0;
float delta_t_s = 0;
float counter0 = 0;
float counter1 = 0;
float counter2 = 0;
int fan_speed=0;
int singleShot_flag=2;
float openTime =0;
float closedTime =0;



double actual_speed0;
double actual_speed1;
double actual_speed2;

double setpoint_speed0 = 0;
double setpoint_speed1 = 0;
double setpoint_speed2 = 0;

double written_speed0 = 0;
double written_speed1 = 0;
double written_speed2 = 0;

Servo motor0;
Servo motor1;
Servo motor2;
Servo fan;
Servo feedtop;
Servo feedbot;

double Kp=2, Ki=5, Kd=1;
PID motor0_PID(&actual_speed0, &written_speed0, &setpoint_speed0, Kp, Ki, Kd, DIRECT);
PID motor1_PID(&actual_speed1, &written_speed1, &setpoint_speed1, Kp, Ki, Kd, DIRECT);
PID motor2_PID(&actual_speed2, &written_speed2, &setpoint_speed2, Kp, Ki, Kd, DIRECT);
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
  fan.attach(fan_pin);
  feedtop.attach(servoTop_pin);
  feedbot.attach(servoBot_pin);


  motor0_PID.SetMode(AUTOMATIC);
  motor1_PID.SetMode(AUTOMATIC);
  motor2_PID.SetMode(AUTOMATIC);
}

void loop() {
  if (Serial.available() > 1) {
    byte data = Serial.read();
    if (data == 's') {
      setpoint_speed0 = 0;
      setpoint_speed1 = 0;
      setpoint_speed2 = 0;    }
    if (data == 'f') {
      setpoint_speed0 = 180;
      setpoint_speed1 = 180;
      setpoint_speed2 = 180;
    }
    if (data == 'u') {
      int tmp = Serial.parseInt();
      setpoint_speed0 = tmp;
      setpoint_speed1 = tmp;
      setpoint_speed2 = tmp;
      tmp = 0;
    }
    if (data == 'a') {
      setpoint_speed0 = Serial.parseInt();
    }
    if (data == 'b') {
      setpoint_speed1 = Serial.parseInt();
    }
    if (data == 'c') {
      setpoint_speed0 = Serial.parseInt();
    }
    if (data == 'w') {
      fan_speed = Serial.parseInt();
    }
    if (data == 'p') {
      use_PID = true;
      Serial.println("PID enabled");
    }
    if (data == 'q') {
      use_PID = false;
      Serial.println("PID disabled");
    }
    if (data == 't') {
      feedtop.write(openedtop);
      delay(200);
      feedtop.write(closedtop);
    }
    if(data=='y'){
      feedbot.write(openedbottom);
      delay(250);
      feedbot.write(closedbottom);
    }
    if(data=='l'){
      singleShot_flag=2;feedbot.write(openedbottom);
      openTime = millis();
      feedtop.write(openedtop);
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
  if(singleShot_flag>0 && millis()>openTime+225){
    singleShot_flag--;
    if(singleShot_flag==1){
    feedtop.write(closedtop);
    openTime=millis();
    feedbot.write(openedbottom);
    }
    else{
    feedbot.write(closedbottom);
    }
    
  }
  if(use_PID){
    motor0_PID.Compute();
    motor1_PID.Compute();
    motor2_PID.Compute();
  }
  else{
    written_speed0 = setpoint_speed0;
    written_speed1 = setpoint_speed1;
    written_speed2 = setpoint_speed2;
  }
  motor0_writeRPM(written_speed0);
  motor1_writeRPM(written_speed1);
  motor2_writeRPM(written_speed2);
  fan_writeRPM(fan_speed);

  
  delay(1);
}
