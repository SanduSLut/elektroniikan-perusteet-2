// D1
int FirstRedPin = 2;
int FirstGreenPin = 3;

// D2
int SecnBluePin = 9;
int SecnRedPin = 10;
int SecnGreenPin = 11;

// D3
int ThrdBluePin = 5;
int ThrdRedPin = 6;
int ThrdGreenPin = 7;

// BUTTONS
int SW1buttonPin = A1;
int SW2buttonPin = A2;
int SW3buttonPin = A3;
int SW4buttonPin = A4;

// WIRES
int blackWirePin = 8;
int whiteWirePin = 12;
int grayWirePin = 13;

//WIRE LAST STATE
int lastWhiteWire;
int lastGrayWire;
int lastBlackWire;


//POTENTIOMETTER
int potPin = A5;

//POT ACTIVATION
int sendPot = false;
unsigned long lastPotTime = 0;
//RED LED TIMER
bool blinkActive = false;
unsigned long blinkStart = 0;
//10 SEC COUNTER
bool countdownActive = false;
long startTime = 0;
const int countdownDuration = 10000; // 10 sec
//BUTTON FOR RGB
bool lastState = HIGH;
unsigned long pressStart = 0;


// ------------------------ SETUP ------------------------
void setup() {
  // Original LEDs
  pinMode(FirstRedPin, OUTPUT);
  pinMode(FirstGreenPin, OUTPUT);

  pinMode(SecnBluePin, OUTPUT);
  pinMode(SecnRedPin, OUTPUT);
  pinMode(SecnGreenPin, OUTPUT);

  pinMode(ThrdBluePin, OUTPUT);
  pinMode(ThrdRedPin, OUTPUT);
  pinMode(ThrdGreenPin, OUTPUT);


  // Buttons
  pinMode(SW1buttonPin, INPUT_PULLUP);
  pinMode(SW2buttonPin, INPUT_PULLUP);
  pinMode(SW3buttonPin, INPUT_PULLUP);
  pinMode(SW4buttonPin, INPUT_PULLUP);

  //WIRE
  pinMode(whiteWirePin, INPUT);
  pinMode(grayWirePin, INPUT);
  pinMode(blackWirePin, INPUT);

  // Default states
  digitalWrite(FirstRedPin, HIGH);
  analogWrite(FirstGreenPin, 255);

  analogWrite(SecnBluePin, 255);
  analogWrite(SecnRedPin, 255);
  analogWrite(SecnGreenPin, 255);

  digitalWrite(ThrdBluePin, HIGH);
  digitalWrite(ThrdRedPin, HIGH);
  digitalWrite(ThrdGreenPin, HIGH);

  lastWhiteWire = digitalRead(whiteWirePin);
  lastGrayWire = digitalRead(grayWirePin);
  lastBlackWire = digitalRead(blackWirePin);

  Serial.begin(9600);
}

// ------------------------ LOOP ------------------------
void loop() {
  handleButtons();
  handleSerial();
  handleBlink();
  handleCountdown();
  handlePot();
  handleRGB();
  checkButton();
  checkWires();
}

// ------------------------ BUTTONS ------------------------
void handleButtons() {
  // BUTTON 1
  static bool SW1lastButtonState = HIGH;
  bool SW1buttonState = digitalRead(SW1buttonPin);
  if (SW1lastButtonState == HIGH && SW1buttonState == LOW) {
    Serial.println("1"); // send event to Python
  }
  SW1lastButtonState = SW1buttonState;

  // BUTTON 4
  static bool SW4lastButtonState = HIGH;
  bool SW4buttonState = digitalRead(SW4buttonPin);
  if (SW4lastButtonState == HIGH && SW4buttonState == LOW) {
    Serial.println("P"); // send event to Python
  }
  SW4lastButtonState = SW4buttonState;
}

// ------------------------ SERIAL ------------------------
#define SERIAL_BUFFER_SIZE 64
char serialBuffer[SERIAL_BUFFER_SIZE];
uint8_t bufferIndex = 0;
String rgbCommand = "";
bool rgbReady = false;

void handleSerial() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\r') continue; // ignore carriage return

    if (c == '\n') { // end of command
      serialBuffer[bufferIndex] = '\0'; // terminate string
      bufferIndex = 0; // reset for next command

      String cmd = String(serialBuffer);  // convert char array to String
      cmd.trim();  // remove whitespace

      //Serial.print("CMD RECEIVED: ");
      //Serial.println(cmd);

      if (cmd.indexOf(',') != -1) { // contains comma => RGB command
        rgbCommand = cmd;   // safely store in String
        rgbReady = true;   // mark ready for processing
      } else {
        handleOtherSerial(cmd);  // handle non-RGB commands
      }
    } 
    else {
      if (bufferIndex < SERIAL_BUFFER_SIZE - 1) {
        serialBuffer[bufferIndex++] = c;
      } else {
        // buffer overflow, reset
        bufferIndex = 0;
      }
    }
  }
}

// ------------------------ EXISTING COMMANDS ------------------------
void handleOtherSerial(String cmd) {
  if (cmd == "RedTimer") { // continuous red blink
    blinkActive = true;
    blinkStart = millis();
    digitalWrite(FirstRedPin, LOW);
  } 
  else if (cmd == "Comp") { // Green ON
    digitalWrite(FirstRedPin, HIGH);
    analogWrite(FirstGreenPin, 0);
    digitalWrite(SecnGreenPin, LOW);
    digitalWrite(ThrdGreenPin, LOW);
  }
  else if (cmd == "TenSec") { // 10-sec countdown
    countdownActive = true;
    startTime = millis();
    analogWrite(FirstGreenPin, 255);  
  }
  else if (cmd == "OpenGraph") { // open graph
    digitalWrite(ThrdRedPin, HIGH);
    digitalWrite(ThrdGreenPin, HIGH);
    digitalWrite(ThrdBluePin, LOW);
  }
  else if (cmd == "CloseGraph") { // close graph
    digitalWrite(ThrdRedPin, HIGH);
    digitalWrite(ThrdGreenPin, HIGH);
    digitalWrite(ThrdBluePin, HIGH);
  }
  else if (cmd == "Correct1") { // correct pot
    digitalWrite(ThrdRedPin, HIGH);
    digitalWrite(ThrdGreenPin, LOW);
    digitalWrite(ThrdBluePin, HIGH);
  }
  else if (cmd == "Wrong1") { // wrong pot
    digitalWrite(ThrdRedPin, LOW);
    digitalWrite(ThrdGreenPin, HIGH);
    digitalWrite(ThrdBluePin, HIGH);
  }
  else if (cmd == "Correct2") { // correct RGB
    digitalWrite(SecnRedPin, HIGH);
    digitalWrite(SecnGreenPin, LOW);
    digitalWrite(SecnBluePin, HIGH);
  }
  else if (cmd == "Wrong2") { // correct RGB
    digitalWrite(SecnRedPin, LOW);
    digitalWrite(SecnGreenPin, HIGH);
    digitalWrite(SecnGreenPin, HIGH);
  }
  else if (cmd == "Explode") { // correct RGB
    explode();
  }
  else if (cmd == "ResetLed") { // resets all leds
    resetleds();
  }

  else if (cmd == "StartGraph") sendPot = true;
  else if (cmd == "EndGraph") sendPot = false;
}

// ------------------------ BLINK ------------------------
void handleBlink() {
  if (blinkActive && millis() - blinkStart >= 500) {
    digitalWrite(FirstRedPin, HIGH);
    blinkActive = false;
  }
}

// ------------------------ COUNTDOWN ------------------------
void handleCountdown() {
  if (countdownActive) {
    unsigned long elapsed = millis() - startTime;
    if (elapsed < countdownDuration) {
      int interval = map(elapsed, 0, countdownDuration, 500, 50);
      static unsigned long lastBlink = 0;
      static bool state = false;
      if (millis() - lastBlink > interval) {
        state = !state;
        digitalWrite(FirstRedPin, state ? LOW : HIGH);
        lastBlink = millis();
      }
    } else {
      countdownActive = false;
      explode(); 
    }
  }
}

// ------------------------ EXPLODE ------------------------
void explode() {
  resetleds();
  
  for (int i = 0; i <= 255; i++) {
    analogWrite(FirstGreenPin, i);
    delay(10);  // controls fade speed
  }

  analogWrite(FirstGreenPin, 255);

  for (int j = 0; j < 4; j++) {
    // Turn all red LEDs ON
    digitalWrite(FirstRedPin, LOW);
    digitalWrite(SecnRedPin, LOW);
    digitalWrite(ThrdRedPin, LOW);
    delay(300);

    // Turn all red LEDs OFF
    digitalWrite(FirstRedPin, HIGH);
    digitalWrite(SecnRedPin, HIGH);
    digitalWrite(ThrdRedPin, HIGH);
    delay(300);
  }
}

// ------------------------ POT ------------------------
void handlePot() {
  static unsigned long lastPotTime = 0;
  if (sendPot && millis() - lastPotTime > 50) { // 20 Hz
    int potValue = analogRead(potPin);
    Serial.println(potValue);
    lastPotTime = millis();
  }
}

// ------------------------ RGB ------------------------
void handleRGB() {
  if (rgbReady) {
    // parse comma-separated RGB
    int firstComma = rgbCommand.indexOf(',');
    int lastComma  = rgbCommand.lastIndexOf(',');

    if (firstComma != -1 && lastComma != -1 && firstComma != lastComma) {
      int r = rgbCommand.substring(0, firstComma).toInt();
      int g = rgbCommand.substring(firstComma + 1, lastComma).toInt();
      int b = rgbCommand.substring(lastComma + 1).toInt();

      r = constrain(r, 0, 255);
      g = constrain(g, 0, 255);
      b = constrain(b, 0, 255);

      // invert if wiring is 5V -> LED -> pin
      r = 255 - r;
      g = 255 - g;
      b = 255 - b;

      /*Serial.print("R:"); Serial.print(r);
      Serial.print(" G:"); Serial.print(g);
      Serial.print(" B:"); Serial.println(b);*/

      analogWrite(SecnRedPin, r);
      analogWrite(SecnGreenPin, g);
      analogWrite(SecnBluePin, b);
    } else {
      //Serial.println("Invalid RGB command");
    }

    rgbReady = false; // mark processed
  }
}

// ------------------------ BUTTON FOR RGB ------------------------
void checkButton() {
  static bool lastReading = HIGH;
  static bool stableState = HIGH;
  static unsigned long lastDebounceTime = 0;

  const unsigned long debounceDelay = 50;

  bool reading = digitalRead(SW3buttonPin);

  // If reading changed, reset timer
  if (reading != lastReading) {
    lastDebounceTime = millis();
  }

  // If stable for long enough → accept it
  if ((millis() - lastDebounceTime) > debounceDelay) {

    if (reading != stableState) {
      stableState = reading;

      // Button pressed
      if (stableState == LOW) {
        pressStart = millis();
      }

      // Button released
      else {
        unsigned long duration = millis() - pressStart;

        if (duration >= 800) {
          Serial.println("HOLD");
        } else {
          Serial.println("PRESS");
        }
      }
    }
  }
  lastReading = reading;
}

void checkWires() {
  int whiteState = digitalRead(whiteWirePin);
  int grayState = digitalRead(grayWirePin);
  int blackState = digitalRead(blackWirePin);

  // Detect CUT (HIGH → LOW)
  if (whiteState == LOW && lastWhiteWire == HIGH) {
    Serial.println("WHITE_CUT");
  }

  if (grayState == LOW && lastGrayWire == HIGH) {
    Serial.println("GRAY_CUT");
  }

  if (blackState == LOW && lastBlackWire == HIGH) {
    Serial.println("BLACK_CUT");
  }

  // Update last states
  lastWhiteWire = whiteState;
  lastGrayWire = grayState;
  lastBlackWire = blackState;
}

void resetleds() {
  digitalWrite(FirstRedPin, HIGH);
  analogWrite(FirstGreenPin, 255);

  digitalWrite(SecnBluePin, HIGH);
  digitalWrite(SecnRedPin, HIGH);
  digitalWrite(SecnGreenPin, HIGH);

  digitalWrite(ThrdBluePin, HIGH);
  digitalWrite(ThrdRedPin, HIGH);
  digitalWrite(ThrdGreenPin, HIGH);
}



