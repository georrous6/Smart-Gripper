#include <LED.h>

LED Led;

void setup() {
  Led.Add(LED1);
  Led.Off(LED1);

#if NUM_LEDS > 1
  Led.Add(LED2);
  Led.Off(LED2);
#endif

  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();
    int blinkCount = 0;

    switch (input) {
      case '0':
        blinkCount = 1;
        break;
      case '1':
        blinkCount = 2;
        break;
      case '2':
        blinkCount = 3;
        break;
      case 'b':
        blinkCount = 4;
        break;
      case 'c':
        blinkCount = 5;
        break;
      default:
        blinkCount = 0;
        break;
    }

    blinkLED(LED1, blinkCount);
  }
}

void blinkLED(int led, int times) {
  for (int i = 0; i < times; i++) {
    Led.On(led);
    delay(300);
    Led.Off(led);
    delay(300);
  }
}
