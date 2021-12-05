int SonarPin = A0;
int sensorValue;
int SonarPin2 = A3;
int sensorValue2;
int SonarPin3 = A5;
int sensorValue3;

void setup() {
  pinMode(SonarPin,INPUT);
  pinMode(SonarPin2,INPUT);
  pinMode(SonarPin3, INPUT);
  Serial.begin(9600);
}

void loop() {
 sensorValue = analogRead(SonarPin) * 0.5;
 sensorValue2 = analogRead(SonarPin2) * 0.5;
 sensorValue3 = analogRead(SonarPin3) * 0.5;
 delay(50);
 Serial.print("L");
 Serial.print(sensorValue);
 Serial.print(",");
 Serial.print(sensorValue2);
 Serial.print(",");
 Serial.print(sensorValue3);
 Serial.print("R");
 Serial.print(" ");
 delay(100);
}
