const byte ledPin = 25;
const byte interruptPin = 20;
volatile byte state = LOW;

float timeee = 0;
float prev_timeee = 0;
float counter = 0;
float delta_t_s = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), tacho, RISING);
}

void loop(){
  detachInterrupt(digitalPinToInterrupt(interruptPin));
  timeee = millis();
  delta_t_s = (timeee - prev_timeee)/1000;
  Serial.println((counter/delta_t_s)*60);
  counter = 0;
  prev_timeee = timeee;
  attachInterrupt(digitalPinToInterrupt(interruptPin), tacho, RISING);
  delay(2000);}

void tacho() {
  counter += 1; 
}
