const byte ledPin = 25;

const byte motor0_interruptPin = 16;
const byte motor1_interruptPin = 18;
const byte motor2_interruptPin = 20;

float current_time = 0;
float prev_time = 0;
float delta_t_s = 0;
float counter0 = 0;
float counter1 = 0;
float counter2 = 0;
int actual_speed0;
int actual_speed1;
int actual_speed2;

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
}

void loop() {
  current_time = millis();
  delta_t_s = (current_time - prev_time)/1000;
  actual_speed0 = (counter0/delta_t_s)*60;
  actual_speed1 = (counter1/delta_t_s)*60;
  actual_speed2 = (counter2/delta_t_s)*60;
  Serial.print(actual_speed0);
  Serial.print(", ");
  Serial.print(actual_speed1);
  Serial.print(", ");
  Serial.println(actual_speed2);
  delay(1000);
}
