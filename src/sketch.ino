#include <Colorduino.h>

#define SERIAL_LEN 5

unsigned char inData[SERIAL_LEN];
unsigned char inChar;
byte index = 0;

void setup()
{
    Serial.begin(9600);
    Colorduino.Init();
    unsigned char whiteBalVal[3] = {36, 63, 63};
    Colorduino.SetWhiteBal(whiteBalVal);
}

void loop()
{
    while (Serial.available() > 0 && index < SERIAL_LEN)
    {
        inChar = Serial.read();
        inData[index++] = inChar;
    }

    if (index == SERIAL_LEN)
    {
        index = 0;
        if (inData[0] == 'F') {
            Colorduino.FlipPage();
        } else {
            Colorduino.SetPixel(
                inData[0], inData[1],
                inData[2], inData[3], inData[4]
            );
        }
    }
}
