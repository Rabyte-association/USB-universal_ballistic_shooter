// software for controling the universal balistic shooter
// using standard esc, hall sensors as tachometers and pid controller
// runs on rpi pico, using the arduino core by Earle F. Philhower is recomended
// by Team Rabyte 2023

#include <Servo.h>
#include <PID_v1.h>

#define MAX_RPM 13500

const byte ledPin = 25;

const byte motor0_interruptPin = 16;
const byte motor1_interruptPin = 18;
const byte motor2_interruptPin = 20;

const byte motor0_pin = 17;
const byte motor1_pin = 19;
const byte motor2_pin = 21;
const byte servoTop_pin = 2;
const byte servoBot_pin = 3;
const byte fan_pin = 1;

// feeder servo positions
const byte closedtop = 170;
const byte openedtop = 100;
const byte closedbottom = 160;
const byte openedbottom = 100;

uint32_t current_time = 0;
uint32_t prev_time = 0;
uint32_t delta_t_s = 0;
uint32_t counter0 = 0;
uint32_t counter1 = 0;
uint32_t counter2 = 0;

int fan_speed = 0;
int singleShot_flag = 1;  // keeps track of the feeder state
uint32_t shootTime = 0;   // keeps track of feeder timing
//uint32_t closedTime = 0;

// mesured speeds
double actual_speed0;
double actual_speed1;
double actual_speed2;
// speed setpoints
double setpoint_speed0 = 0;
double setpoint_speed1 = 0;
double setpoint_speed2 = 0;
// speed thats written to escs
double written_speed0 = 0;
double written_speed1 = 0;
double written_speed2 = 0;

Servo motor0;
Servo motor1;
Servo motor2;
Servo fan;
Servo feedtop;
Servo feedbot;

//  pid init
double Kp = 0.05, Ki = 0, Kd = 0.05;
PID motor0_PID(&actual_speed0, &written_speed0, &setpoint_speed0, Kp, Ki, Kd, DIRECT);
PID motor1_PID(&actual_speed1, &written_speed1, &setpoint_speed1, Kp, Ki, Kd, DIRECT);
PID motor2_PID(&actual_speed2, &written_speed2, &setpoint_speed2, Kp, Ki, Kd, DIRECT);
bool use_PID = false;

// time beatweeen speed mesourments
// for experimental use
int sampling_delay = 100;

// interrupt routines
// with filtring garbage data, that is generated by the ir sensors
long last_poulse0 = 100;
long courrent_poulse0;
void tacho0() {
  courrent_poulse0 = micros();
  if ((courrent_poulse0 - last_poulse0) >= 300) {
    counter0 += 1;
  }
  last_poulse0 = courrent_poulse0;
}

long last_poulse1 = 100;
long courrent_poulse1;
void tacho1() {
  courrent_poulse1 = micros();
  if ((courrent_poulse1 - last_poulse1) >= 300) {
    counter1 += 1;
  }
  last_poulse1 = courrent_poulse1;
}

long last_poulse2 = 100;
long courrent_poulse2;
void tacho2() {
  courrent_poulse2 = micros();
  if ((courrent_poulse2 - last_poulse2) >= 300) {
    counter2 += 1;
  }
  last_poulse2 = courrent_poulse2;
}


long beginig_calculation = 0;

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
  motor0.write(90);
  motor1.write(0);
  motor2.write(0);

  fan.attach(fan_pin);

  feedtop.attach(servoTop_pin);
  feedbot.attach(servoBot_pin);
  feedtop.write(closedtop);
  feedtop.write(closedbottom);
  feedbot.write(openedbottom);
  feedtop.write(closedtop);

  motor0_PID.SetMode(AUTOMATIC);
  motor1_PID.SetMode(AUTOMATIC);
  motor2_PID.SetMode(AUTOMATIC);
}

void setup1() {

}

void loop() {

  // detaching the interrupts
  // so the calculations don't get messed up
  detachInterrupt(digitalPinToInterrupt(motor0_interruptPin));
  detachInterrupt(digitalPinToInterrupt(motor1_interruptPin));
  detachInterrupt(digitalPinToInterrupt(motor2_interruptPin));

  // for experimental use
  // mesouring how long it take to claculate everythong
  beginig_calculation = millis();

  current_time = millis();
  delta_t_s = (current_time - prev_time);

  actual_speed0 = (counter0 * 7500 / delta_t_s);
  actual_speed1 = (counter1 * 7500 / delta_t_s);
  actual_speed2 = (counter2 * 7500 / delta_t_s);

  counter0 = 0;
  counter1 = 0;
  counter2 = 0;
  prev_time = current_time;

  print_debug();

  if (use_PID) {
    motor0_PID.Compute();
    motor1_PID.Compute();
    motor2_PID.Compute();

    // limiting the motors values to 70 out of 180
    // so the machine does not destroy itself
    if (written_speed0 >= 70) {
      written_speed0 = 70;
    }
    if (written_speed1 >= 70) {
      written_speed1 = 70;
    }
    if (written_speed1 >= 70) {
      written_speed1 = 70;
    }
  }
  else {
    written_speed0 = setpoint_speed0;
    written_speed1 = setpoint_speed1;
    written_speed2 = setpoint_speed2;
  }
  motor0_writeRPM(written_speed0);
  motor1_writeRPM(written_speed1);
  motor2_writeRPM(written_speed2);
  fan_writeRPM(fan_speed);

  // printing the mesoured time of calculation
  // NOT FOR PRODUCTION!
  //  Serial.println(beginig_calculation - millis());

  // attaching the instrrupts back again
  attachInterrupt(digitalPinToInterrupt(motor0_interruptPin), tacho0, RISING);
  attachInterrupt(digitalPinToInterrupt(motor1_interruptPin), tacho1, RISING);
  attachInterrupt(digitalPinToInterrupt(motor2_interruptPin), tacho2, RISING);

  delay(sampling_delay);
}

void loop1() {
  // using the second core of rp2040
  // so we can safly use delays in the loop

  // reading the data, using our famous protocol
  if (Serial.available() > 1) {
    byte data = Serial.read();
    if (data == 's') {
      setpoint_speed0 = 0;
      setpoint_speed1 = 0;
      setpoint_speed2 = 0;
      fan_speed = 0;
    }
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
      setpoint_speed2 = Serial.parseInt();
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
    if (data == 'l') {
      singleShot_flag = 1;
    }
    if (data == 't') {
      sampling_delay = Serial.parseInt();
    }
  }

  // feeder, driving the servos and waiting
  if (singleShot_flag == 1) {
    feedtop.write(openedtop);
    shootTime = millis();
    singleShot_flag = 2;
  }
  if (singleShot_flag == 2 && (millis() - shootTime) >= 200) {
    feedtop.write(closedtop);
    shootTime = millis();
    singleShot_flag = 3;
  }
  if (singleShot_flag == 3 && (millis() - shootTime) >= 200) {
    feedbot.write(openedbottom);
    shootTime = millis();
    singleShot_flag = 4;
  }
  if (singleShot_flag == 4 && (millis() - shootTime) >= 100) {
    feedbot.write(closedbottom);
    shootTime = millis();
    singleShot_flag = 0;
  }
}
