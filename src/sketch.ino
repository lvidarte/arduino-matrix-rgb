#include <Colorduino.h>

#define SERIAL_LEN 2

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

        int x = inData[0] & 7;
        int y = ((inData[0] >> 3) & 7);
        int r = (inData[0] >> 6) | (2 << (inData[1] & 1));
        int g = (inData[1] >> 1) & 7;
        int b = (inData[1] >> 4) & 7;
        int f = inData[1] >> 7;

        Serial.println(x);
        Serial.println(y);
        Serial.println(r);
        Serial.println(g);
        Serial.println(b);
        Serial.println(f);

        Colorduino.SetPixel(
            x, y,
            map(r, 0, 7, 0, 255),
            map(g, 0, 7, 0, 255),
            map(b, 0, 7, 0, 255)
        );

        if (f) {
            Colorduino.FlipPage();
        }
    }
}
