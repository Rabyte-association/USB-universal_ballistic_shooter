void print_debug() {
  Serial.print(setpoint_speed0);
  Serial.print(", ");
  Serial.print(setpoint_speed1);
  Serial.print(", ");
  Serial.print(setpoint_speed2);
  Serial.print(", ");
  Serial.print(actual_speed0);
  Serial.print(", ");
  Serial.print(actual_speed1);
  Serial.print(", ");
  Serial.println(actual_speed2);
  //  Serial.print(", ");
  //  Serial.println(fan_speed);
}
void fan_writeRPM(int percent) {
  int out_deg = map(percent, 0, 100, 0, 180);
  if (out_deg > 180) out_deg = 180;
  fan.write(out_deg);
}

void motor0_writeRPM(double rpm) {
  //  int out_deg = map(rpm, 0, MAX_RPM, 0, 180);
  //  if(out_deg > 180) out_deg = 180;
  int out_deg = map(rpm, -180, 180, 0, 180);
  motor0.write(rpm);
}
void motor1_writeRPM(double rpm) {
  //  int out_deg = map(rpm, 0, MAX_RPM, 0, 180);
  //  if(out_deg > 180) out_deg = 180;
  int out_deg = rpm;
  motor1.write(out_deg);
}
void motor2_writeRPM(double rpm) {
  //  int out_deg = map(rpm, 0, MAX_RPM, 0, 180);
  //  if(out_deg > 180) out_deg = 180;
  int out_deg = rpm;
  motor2.write(out_deg);
}
