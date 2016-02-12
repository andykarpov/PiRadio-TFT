#include <Wire.h>

#include <Encoder.h>
#include <Button.h>

Encoder enc1(3, 5);
Encoder enc2(2, 4);

Button  btn1(6, PULLUP);
Button  btn2(7, PULLUP);
Button  btn3(8, PULLUP);
Button  btn4(9, PULLUP);
Button  btn5(10, PULLUP);
Button  btn6(11, PULLUP);
Button  btn7(12, PULLUP);
Button  btn8(13, PULLUP);

#define I2C_SLAVE_ADDRESS  0x40
#define TWI_FREQ_SETTING         400000L       // 400KHz for I2C
#define CPU_FREQ                 8000000L     // 16MHz

byte last_command = 0;

volatile byte val1 = 0;
volatile byte val1_min = 0;
volatile byte val1_max = 100;
volatile int reading1 = 0;

volatile byte val2 = 0;
volatile byte val2_min = 0;
volatile byte val2_max = 100;
volatile int reading2 = 0;

volatile byte buttons = 0;
int argsCnt = 0;
byte i2cArgs[32];
uint8_t response[32];

extern const byte supportedI2Ccmd[] = { 
  1
};

void setup() {
    // >> starting i2c
  TWBR = ((CPU_FREQ / TWI_FREQ_SETTING) - 16) / 2;
  Wire.begin(I2C_SLAVE_ADDRESS); // join i2c bus with address 0x50
  Wire.onRequest(requestEvent); // register event
  Wire.onReceive(receiveEvent); // register event
}

void loop() {
  
  reading1 = enc1.read() / 4;
  reading2 = enc2.read() / 4;
  buttons = btn1.isPressed() |
           (btn2.isPressed() << 1) |
           (btn3.isPressed() << 2) |
           (btn4.isPressed() << 3) |
           (btn5.isPressed() << 4) |
           (btn6.isPressed() << 5) |
           (btn7.isPressed() << 6) |
           (btn8.isPressed() << 7);

  if (reading1 > val1_max) {
    reading1 = val1_max;
    enc1.write(reading1 * 4);
  }
  if (reading1 < val1_min) {
    reading1 = val1_min;
    enc1.write(reading1 * 4);
  }

  if (reading2 > val2_max) {
    reading2 = val2_max;
    enc2.write(reading2 * 4);
  }
  if (reading2 < val2_min) {
    reading2 = val2_min;
    enc2.write(reading2 * 4);
  }

  response[0] = (byte) reading1;
  response[1] = (byte) reading2;
  response[2] = (byte) buttons;           
}

// receive command + 6 bytes from master min1:max1:val1:min2:max2:val2
void receiveEvent(int howMany) {

  int cmdRcvd = -1;
  int argIndex = -1; 
  argsCnt = 0;

  if (Wire.available()){
    last_command = Wire.read();                 // receive first byte - command assumed
    while(Wire.available()){               // receive rest of tramsmission from master assuming arguments to the command
      if (argIndex < 32){
        argIndex++;
        i2cArgs[argIndex] = Wire.read();
      }
      else{
        ; // implement logging error: "too many arguments"
      }
      argsCnt = argIndex+1;  
    }
  }
  else{
    // implement logging error: "empty request"
    return;
  }
  // validating command is supported by slave
  int fcnt = -1;
  for (int i = 0; i < sizeof(supportedI2Ccmd); i++) {
    if (supportedI2Ccmd[i] == last_command) {
      fcnt = i;
    }
  }

  if (fcnt<0){
    // implement logging error: "command not supported"
    return;
  }

  val1_min = i2cArgs[0];
  val1_max = i2cArgs[1];
  val1 = i2cArgs[2];
  val2_min = i2cArgs[3];
  val2_max = i2cArgs[4];
  val2 = i2cArgs[5];

  enc1.write(val1 * 4);
  enc2.write(val2 * 4);
    
}

// return 3 bytes of readings
void requestEvent() {
  Wire.write(response, 3);
}
