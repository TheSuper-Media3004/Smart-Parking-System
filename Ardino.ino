#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// LCD setup — use the correct I2C address (0x27 or 0x3F)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// IR sensor pins
const int irSensorEntry = 2; // Before gate (entry)
const int irSensorExit = 3;  // After gate (exit)

// LED pins
const int redLED = 6;
const int greenLED = 7;

// Servo pin
const int servoPin = 9;
Servo gateServo;

// Total parking slots
const int totalSlots = 4;
int parkedCars = 0;

// --- Gate control functions ---
void gateLock() {
  gateServo.write(90); // Closed position
  digitalWrite(redLED, HIGH);
  digitalWrite(greenLED, LOW);
}

void openGate() {
  gateServo.write(0); // Open position
  digitalWrite(redLED, LOW);
  digitalWrite(greenLED, HIGH);
}

void setup() {
  // Initialize LCD
  lcd.init();           // initialize the LCD
  lcd.backlight();      // turn on backlight
  lcd.setCursor(0, 0);
  lcd.print("Smart Parking");
  delay(2000);
  lcd.clear();

  // Pin setup
  pinMode(irSensorEntry, INPUT);
  pinMode(irSensorExit, INPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  // Servo setup
  gateServo.attach(servoPin);
  gateLock();

  lcd.setCursor(0, 0);
  lcd.print("Slot Left: ");
  lcd.print(totalSlots - parkedCars);
}

void loop() {
  int entryState = digitalRead(irSensorEntry);
  int exitState = digitalRead(irSensorExit);

  lcd.setCursor(0, 0);
  lcd.print("Slot Left: ");
  lcd.print(totalSlots - parkedCars);
  lcd.print("   "); // Clear old digits

  // --- Car entering ---
  if (entryState == LOW) {  // Car detected at entry
    delay(100); // debounce
    if (parkedCars < totalSlots) {
      openGate();
      lcd.setCursor(0, 1);
      lcd.print("Car Entering...   ");

      // Wait until car passes entry and triggers exit sensor
      while (digitalRead(irSensorExit) == HIGH);
      delay(300);
      while (digitalRead(irSensorExit) == LOW);
      delay(1000);

      parkedCars++;
      gateLock();
      lcd.clear();
    } else {
      lcd.setCursor(0, 1);
      lcd.print("No Space Left     ");
      delay(2000);
      lcd.clear();
    }
  }

  // --- Car exiting ---
  if (exitState == LOW) {  // Car detected at exit
    delay(100); // debounce
    if (parkedCars > 0) {
      openGate();
      lcd.setCursor(0, 1);
      lcd.print("Car Exiting...    ");

      // Wait until car passes entry sensor
      while (digitalRead(irSensorEntry) == HIGH);
      delay(300);
      while (digitalRead(irSensorEntry) == LOW);
      delay(1000);

      parkedCars--;
      gateLock();
      lcd.clear();
    }
  }

  delay(100);
}
