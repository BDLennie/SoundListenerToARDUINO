bool sound = false;
String tempRead;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(13,OUTPUT);
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

    digitalWrite(LED_BUILTIN, sound ? HIGH : LOW);
    digitalWrite(13, sound ? HIGH : LOW);
  }
}