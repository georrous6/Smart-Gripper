#include "TLE5012Sensor.h"  // angle sensor
#include "TLx493D_inc.hpp"  // magnetic sensor
#include "config.h"
#include <SimpleFOC.h>

// Define SPI pins for TLE5012 sensor
#define PIN_SPI1_SS0 94
#define PIN_SPI1_MOSI 69
#define PIN_SPI1_MISO 95
#define PIN_SPI1_SCK 68

// SPI & sensor instances
tle5012::SPIClass3W tle5012::SPI3W1(2);
TLE5012Sensor tle5012Sensor(&SPI3W1, PIN_SPI1_SS0, PIN_SPI1_MISO, PIN_SPI1_MOSI, PIN_SPI1_SCK);

// Motor and driver
BLDCMotor motor = BLDCMotor(7, 0.24, 360, 0.000133);
const int U = 11, V = 10, W = 9;
const int EN_U = 6, EN_V = 5, EN_W = 3;
BLDCDriver3PWM driver = BLDCDriver3PWM(U, V, W, EN_U, EN_V, EN_W);

float target_voltage = 0;
float initialAngle = 0;

enum GripperMode {
  MODE_IDLE,
  MODE_CLOSE_GRIP,
  MODE_OPEN_GRIP
};

GripperMode gripperMode = MODE_IDLE;

#if ENABLE_MAGNETIC_SENSOR
using namespace ifx::tlx493d;
TLx493D_A2B6 dut(Wire1, TLx493D_IIC_ADDR_A0_e);
const int CALIBRATION_SAMPLES = 20;
double xOffset = 0, yOffset = 0, zOffset = 0;
#endif

#if ENABLE_COMMANDER
Commander command = Commander(Serial);
void doTarget(char *cmd) { command.scalar(&target_voltage, cmd); }
#endif

bool lastButton1State = HIGH;
bool lastButton2State = HIGH;

// PID parameters
float kp = 1.0;
float ki = 0.0;
float kd = 0.0;
float error_integral = 0;
float last_error = 0;
float threshold = 0.8;  // Norm threshold (adjust to your use case)
unsigned long last_pid_time = 0;

char serialCommand = '0';

void processCommand(char cmd) {
  switch(cmd) {
    case '0':
      gripperMode = MODE_IDLE;
      break;
    case '1':
      gripperMode = MODE_CLOSE_GRIP;
      break;
    case '2':
      gripperMode = MODE_OPEN_GRIP;
      break;
  }
}

void setup() {
  Serial.begin(115200);
  SimpleFOCDebug::enable(&Serial);

  tle5012Sensor.init();
  motor.linkSensor(&tle5012Sensor);

  driver.voltage_power_supply = 12;
  driver.voltage_limit = 6;
  if (!driver.init()) {
    Serial.println("Driver init failed!");
    return;
  }
  motor.linkDriver(&driver);

  motor.voltage_sensor_align = 2;
  motor.foc_modulation = FOCModulationType::SpaceVectorPWM;
  motor.controller = MotionControlType::torque;
  motor.init();
  motor.initFOC();
  Serial.println(F("Motor ready."));

  initialAngle = tle5012Sensor.getSensorAngle();

#if ENABLE_MAGNETIC_SENSOR
  dut.begin();
  calibrateSensor();
  Serial.println("3D magnetic sensor Calibration completed.");

  pinMode(BUTTON1, INPUT);
  pinMode(BUTTON2, INPUT);
#endif

  Serial.println("setup done.");

#if ENABLE_COMMANDER
  command.add('T', doTarget, "target voltage");
  Serial.println(F("Set the target voltage using serial terminal:"));
#endif
  _delay(1000);
}

void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'T') {
      while (!Serial.available()) {
        delay(100);
      }
      serialCommand = Serial.read();
      processCommand(serialCommand);
    }
  }

#if ENABLE_MAGNETIC_SENSOR
  bool currentButton1State = digitalRead(BUTTON1);
  bool currentButton2State = digitalRead(BUTTON2);

  if (currentButton1State == LOW && lastButton1State == HIGH) {
    gripperMode = (gripperMode == MODE_CLOSE_GRIP) ? MODE_IDLE : MODE_CLOSE_GRIP;
    delay(50);
  }

  if (currentButton2State == LOW && lastButton2State == HIGH) {
    gripperMode = (gripperMode == MODE_OPEN_GRIP) ? MODE_IDLE : MODE_OPEN_GRIP;
    delay(50);
  }

  lastButton1State = currentButton1State;
  lastButton2State = currentButton2State;
  //Serial.print("Mode: "); Serial.print(gripperMode); Serial.println("");

  if (gripperMode == MODE_CLOSE_GRIP) {
    double x, y, z;
    dut.setSensitivity(TLx493D_FULL_RANGE_e);
    dut.getMagneticField(&x, &y, &z);
    x -= xOffset; y -= yOffset; z -= zOffset;
    closeGripperControl(x, y, z);
  } 
  else if (gripperMode == MODE_OPEN_GRIP) {
    openGripperControl();
  }
  else {
    target_voltage = 0;
  }


#endif

  tle5012Sensor.update();
#if ENABLE_READ_ANGLE
  // Serial.println(tle5012Sensor.getSensorAngle());
#endif

  motor.loopFOC();
  motor.move(target_voltage);

#if ENABLE_COMMANDER
  command.run();
#endif
}

void closeGripperControl(double x, double y, double z) {
  float norm = sqrt(x * x + y * y + z * z);
  float error = norm - threshold;

  if (last_pid_time < 1e-6f) {
    last_pid_time = millis();
    return;
  }

  unsigned long now = millis();
  float dt = (now - last_pid_time) / 1000.0;

  if (dt > 0) {
    error_integral += error * dt;
    float derivative = (error - last_error) / dt;
    float pid_output = kp * error + ki * error_integral + kd * derivative;

    target_voltage = constrain(pid_output, -6, 6);
    last_error = error;
    last_pid_time = now;
  }

  // Serial.print("Magnitude norm: "); Serial.print(norm); 
  // Serial.print(", target voltage: "); Serial.print(target_voltage); Serial.println("");
}

void openGripperControl() {
  // float sensorAngle = tle5012Sensor.getSensorAngle();
  target_voltage = 0.5;
  // Serial.print("Initial angle: "); Serial.print(initialAngle); Serial.print(" sensor angle: "); Serial.print(sensorAngle); Serial.println("");
}

#if ENABLE_MAGNETIC_SENSOR
void calibrateSensor() {
  double sumX = 0, sumY = 0, sumZ = 0;
  Serial.println("=== Start of Calibration ===");
  for (int i = 0; i < CALIBRATION_SAMPLES; ++i) {
    double temp, valX, valY, valZ;
    dut.getMagneticFieldAndTemperature(&valX, &valY, &valZ, &temp);
    sumX += valX;
    sumY += valY;
    sumZ += valZ;
    delay(10);
  }
  xOffset = sumX / CALIBRATION_SAMPLES;
  yOffset = sumY / CALIBRATION_SAMPLES;
  zOffset = sumZ / CALIBRATION_SAMPLES;
  Serial.println("=== End of Calibration ===");
}
#endif
