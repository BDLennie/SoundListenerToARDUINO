bool sound = false;
bool prevState = false;   // tracks previous "True"/not-"True" state
String tempRead;
int relayPin = 7;
unsigned long lastTime = 0;
const long duration = 2000;

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
}

void loop() {
  if (Serial.available()) {
    tempRead = Serial.readStringUntil('\n');
    tempRead.trim();

    bool currentState = (tempRead == "True");

    // Only trigger on the rising edge (transition into "True")
    if (currentState && !prevState) {
      sound = true;
      lastTime = millis();
    }

    prevState = currentState;
  }

  // Runs every loop, regardless of whether serial data arrived
  if (sound && (millis() - lastTime >= duration)) {
    sound = false;
  }

  digitalWrite(relayPin, sound ? HIGH : LOW);
}