bool sound = false;
String tempRead;
int relayPin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(relayPin,OUTPUT);
}

void loop() {
  if (Serial.available()) {
    tempRead = Serial.readStringUntil('\n');
    tempRead.trim();

    if (tempRead == "True") {
      sound = true;
    } else if (tempRead == "False") {
      sound = false;
    }

    digitalWrite(relayPin, sound ? HIGH : LOW);
  }
}