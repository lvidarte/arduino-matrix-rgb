#include <Colorduino.h>
#include <SoftwareSerial.h>

#define SERIAL_LEN 2

// Commands
#define CMD_FLIP_PAGE 0
#define CMD_OFFSCREEN_FRAME_BUFFER 1
#define CMD_ACTIVE_FRAME_BUFFER 2

unsigned char inData[SERIAL_LEN];
unsigned char inChar;

byte index = 0;
byte actual_frame_buffer = 1;

void log_command(char *command);
void log_led_settings(int x, int y,
                      int r, int g, int b,
                      int red, int green, int blue);

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

        int command_mode = inData[1] >> 7;

        if (command_mode) {

            if (inData[0] == CMD_FLIP_PAGE) {
                log_command("flip page");
                Colorduino.FlipPage();
            }
            if (inData[0] == CMD_OFFSCREEN_FRAME_BUFFER) {
                log_command("set offscreen frame buffer");
                actual_frame_buffer = CMD_OFFSCREEN_FRAME_BUFFER;
            }
            if (inData[0] == CMD_ACTIVE_FRAME_BUFFER) {
                log_command("set active frame buffer");
                actual_frame_buffer = CMD_ACTIVE_FRAME_BUFFER;
            }

        } else {

            int x = inData[0] & 7;
            int y = ((inData[0] >> 3) & 7);
            int r = (inData[0] >> 6) | ((inData[1] & 1) << 2);
            int g = (inData[1] >> 1) & 7;
            int b = (inData[1] >> 4) & 7;

            int red = map(r, 0, 7, 0, 255);
            int green = map(g, 0, 7, 0, 255);
            int blue = map(b, 0, 7, 0, 255);

            log_led_settings(x, y, r, g, b, red, green, blue);

            if (actual_frame_buffer == CMD_OFFSCREEN_FRAME_BUFFER) {
                Colorduino.SetPixel(x, y, red, green, blue);
            }
            if (actual_frame_buffer == CMD_ACTIVE_FRAME_BUFFER) {
                ColorRGB *p = Colorduino.GetDrawPixel(x, y);
                p->r = red;
                p->g = green;
                p->b = blue;
            }
        }

    }
}

void log_command(char *command)
{
    Serial.print("command: ");
    Serial.println(command);
}

void log_led_settings(int x, int y,
                      int r, int g, int b,
                      int red, int green, int blue)
{

    Serial.print("pos[");
    Serial.print(x);
    Serial.print(", ");
    Serial.print(y);
    Serial.print("] vals[");

    Serial.print(r);
    Serial.print(", ");
    Serial.print(g);
    Serial.print(", ");
    Serial.print(b);
    Serial.print("] rgb(");

    Serial.print(red);
    Serial.print(", ");
    Serial.print(green);
    Serial.print(", ");
    Serial.print(blue);
    Serial.println(") ");
}
