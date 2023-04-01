void print_debug(){
  Serial.print(actual_speed0);
  Serial.print(", ");
  Serial.print(actual_speed1);
  Serial.print(", ");
  Serial.println(actual_speed2);

  Serial.print(setpiont_speed0);
  Serial.print(", ");
  Serial.print(setpiont_speed1);
  Serial.print(", ");
  Serial.println(setpiont_speed2);
}

void motor0_writeRPM(double rpm){
  int out_rpm = map(rpm, 0, MAX_RPM, 0, 180); 
  if(out_rpm > 180) out_rpm = 180;
  motor0.write(out_rpm);
}

void motor1_writeRPM(double rpm){
  int out_rpm = map(rpm, 0, MAX_RPM, 0, 180); 
  if(out_rpm > 180) out_rpm = 180;
  motor1.write(out_rpm);
}

void motor2_writeRPM(double rpm){
  int out_rpm = map(rpm, 0, MAX_RPM, 0, 180); 
  if(out_rpm > 180) out_rpm = 180;
  motor2.write(out_rpm);
}
