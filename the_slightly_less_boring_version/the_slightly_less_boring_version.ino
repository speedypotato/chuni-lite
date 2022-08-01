// Basic Chunithm Slider Companion (IR, RGB, Billboard)
// Based off @mon the_boring_version, written by @SpeedyPotato

#include <Keyboard.h>
#include <FastLED.h>

#define NUM_IR 6          // Number of IR Beams
#define IR_THRESHOLD 0.6  // % required to trigger
struct {
  uint8_t irPin;    // LED Pin
  uint8_t recPin;   // Photodiode Pin
  uint32_t val;     // Caliibrated Value
  char key;         // Output Keystroke
} beams[NUM_IR] = {
  6, A9, 0, '4',  // 1
  16, A1, 0, '7', // 4
  7, A10, 0, '5', // 2
  14, A2, 0, '8', // 5
  8, A0, 0, '6',  // 3
  15, A3, 0, '9', // 6
};
// Above LEDS are 1(lowest) to 6(highest) - they are out of order for optimal polling

#define COIN 5        // Coin Pin
#define COIN_KEY '3'  // Output Keystroke

#define LEFT_PIN      3
#define RIGHT_PIN     4
#define NUM_LEDS 3
#define LED_NUM_MAX 66

// side 0: 5*10 billboard and 3 air strings
#define BOARD0_LEDS (5*10 + 3)
// side 1: 6*10 billboard and 3 air strings
#define BOARD1_LEDS (6*10 + 3)
// side 2: slider, don't care
struct {
  uint8_t board;   // LED output the data is for (0-1: billboard, 2: slider)
  CRGB data[LED_NUM_MAX]; // Buffer for LEDs
} ledData;

size_t off;
bool escape;

#define CALIBRATION_CYCLES 10

/**
   IR Beam Calibration Procedure
*/
void beamCalibration() {
  for (int i = 0; i < CALIBRATION_CYCLES; i++) {
    for (int j = 0; j < NUM_IR; j++) {
      beams[j].val += readBeam(j);
    }
  }
  for (int i = 0; i < NUM_IR; i++) {
    beams[i].val /= CALIBRATION_CYCLES;
  }
}

/**
   Reads output from a single beam
*/
int readBeam(int beamIndex) {
  digitalWrite(beams[beamIndex].irPin, HIGH);
  delayMicroseconds(200); //300 seems the highest that's needed, can go lower maybe
  int result = analogRead(beams[beamIndex].recPin);
  Serial.print(String(result) + "\t");
  digitalWrite(beams[beamIndex].irPin, LOW);
  return result;
}

void setup() {
  // data from game
  Serial.begin(115200);
  Keyboard.begin();

  for (uint8_t i = 0; i < NUM_IR; i++) {
    pinMode(beams[i].recPin, INPUT);
    pinMode(beams[i].irPin, OUTPUT);
  }
  beamCalibration();

  pinMode(COIN, INPUT_PULLUP);

  // just steal the raw array values lol
  FastLED.addLeds<WS2812B, LEFT_PIN, RGB>(&ledData.data[50], NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<WS2812B, RIGHT_PIN, RGB>(&ledData.data[60], NUM_LEDS).setCorrection( TypicalLEDStrip );
  // initialize to white
  fill_solid(&ledData.data[50], NUM_LEDS, CRGB::White);
  fill_solid(&ledData.data[60], NUM_LEDS, CRGB::White);
  FastLED.show();
}

void loop() {
  for (uint8_t i = 0; i < NUM_IR; i++) {
    if (readBeam(i) < (IR_THRESHOLD * beams[i].val)) {
      Keyboard.press(beams[i].key);
    } else {
      Keyboard.release(beams[i].key);
    }
  }
  Serial.println();

  if(digitalRead(COIN) == LOW) {
    Keyboard.press(COIN_KEY);
  } else {
    Keyboard.release(COIN_KEY);
  }

  while (Serial.available()) {
    uint8_t b = Serial.read();

    if (b == 0xE0) {
      if (off > 2) {
        size_t len = off - 1;
        if (ledData.board == 0 && len == 3 * BOARD0_LEDS) {
          FastLED[0].showLeds();
        } else if (ledData.board == 1 && len == 3 * BOARD1_LEDS) {
          FastLED[1].showLeds();
        }
      }
      escape = false;
      off = 0;
      continue;
    }

    if (b == 0xD0) {
      escape = true;
      continue;
    }

    if (escape) {
      escape = false;
      b += 1;
    }

    if (off < sizeof(ledData)) {
      ((uint8_t*)&ledData)[off++] = b;
    }
  }
}
