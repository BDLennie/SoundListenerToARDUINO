bool sound = false;

bool prevState = false;
bool buttonTriggered = false;

String tempRead;

int relayPin = 7;
int buttonPin = 5;

unsigned long lastTime = 0;
const unsigned long duration = 2000;

void setup() {
  Serial.begin(9600);

  pinMode(relayPin, OUTPUT);
  pinMode(buttonPin, INPUT);

  digitalWrite(relayPin, LOW);
}

void loop() {

  // SERIAL
  if (Serial.available()) {
    tempRead = Serial.readStringUntil('\n');
    tempRead.trim();

    bool currentState = (tempRead == "True");

    if (currentState && !prevState) {
      sound = true;
      lastTime = millis();
    }

    prevState = currentState;
  }


  // BUTTON
  bool buttonState = digitalRead(buttonPin);

  // Knop ingedrukt → slechts één keer triggeren
  if (buttonState && !buttonTriggered) {
    sound = true;
    lastTime = millis();

    buttonTriggered = true;
  }

  // Pas opnieuw mogen triggeren nadat knop losgelaten is
  if (!buttonState) {
    buttonTriggered = false;
  }


  // TIMER
  if (sound && millis() - lastTime >= duration) {
    sound = false;
  }

  digitalWrite(relayPin, sound ? HIGH : LOW);
}
