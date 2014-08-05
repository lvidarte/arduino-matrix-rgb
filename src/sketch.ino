#include <Colorduino.h>
#include <SoftwareSerial.h>

#define SCREEN_WIDTH  8
#define SCREEN_HEIGHT 8
#define MASK_WIDTH    B111
#define MASK_HEIGHT   B111

/**
 * Commands
 */
#define CMD_CLEAR B0000
#define CMD_FLIP  B0001
#define CMD_SET_X B1000
#define CMD_SET_Y B1001
#define CMD_SET_R B1010
#define CMD_SET_G B1011
#define CMD_SET_B B1100
#define CMD_FILL  B1111

/**
 * Params
 */
#define PARAM_OBJ_LED B00
#define PARAM_OBJ_COL B01
#define PARAM_OBJ_ROW B10
#define PARAM_OBJ_ALL B11
#define PARAM_PAGE_BG B0
#define PARAM_PAGE_FG B1
#define PARAM_NORST   B0
#define PARAM_RESET   B1

/**
 * Led state
 */
typedef struct {
    byte x = 0;
    byte y = 0;
    byte r = 0;
    byte g = 0;
    byte b = 0;
} Led;

Led led;

/**
 *
 */
char log_buffer[48];


/**
 * Functions
 */
void set_x(byte param)
{
    led.x = get_pos(param, MASK_WIDTH);
    log_set('x', led.x);
}

void set_y(byte param)
{
    led.y = get_pos(param, MASK_HEIGHT);
    log_set('y', led.y);
}

void set_r(byte param)
{
    led.r = get_color(param);
    log_set('r', led.r);
}

void set_g(byte param)
{
    led.g = get_color(param);
    log_set('g', led.g);
}

void set_b(byte param)
{
    led.b = get_color(param);
    log_set('b', led.b);
}

void flip_page()
{
    Colorduino.FlipPage();
    log_text("flip_page()");
}

int get_pos(byte value, byte mask)
{
    return value & mask;
}

int get_color(byte value)
{
    return map(value, 0, 15, 0, 255);
}

void set_color_led(byte x, byte y, byte r, byte g, byte b, byte page)
{
    switch (page)
    {
        case PARAM_PAGE_BG:
            Colorduino.SetPixel(x, y, r, g, b);
            break;

        case PARAM_PAGE_FG:
            PixelRGB *p = Colorduino.GetDrawPixel(x, y);
            p->r = r;
            p->g = g;
            p->b = b;
            break;
    }
}

void set_color_row(byte y, byte r, byte g, byte b, byte page = PARAM_PAGE_BG)
{
    for (byte x = 0; x < SCREEN_WIDTH; x++)
    {
        set_color_led(x, y, r, g, b, page);
    }
}

void set_color_col(byte x, byte r, byte g, byte b, byte page = PARAM_PAGE_BG)
{
    for (byte y = 0; y < SCREEN_HEIGHT; y++)
    {
        set_color_led(x, y, r, g, b, page);
    }
}

void set_color_all(byte r, byte g, byte b, byte page = PARAM_PAGE_BG)
{
    for (byte x = 0; x < SCREEN_WIDTH; x++)
    {
        for (byte y = 0; y < SCREEN_HEIGHT; y++)
        {
            set_color_led(x, y, r, g, b, page);
        }
    }
}

void set_color(byte obj, byte r, byte g, byte b, byte page = PARAM_PAGE_BG)
{
    switch (obj)
    {
        case PARAM_OBJ_LED:
            set_color_led(led.x, led.y, r, g, b, page);
            break;
        case PARAM_OBJ_ROW:
            set_color_row(led.y, r, g, b, page);
            break;
        case PARAM_OBJ_COL:
            set_color_col(led.x, r, g, b, page);
            break;
        case PARAM_OBJ_ALL:
            set_color_all(r, g, b, page);
            break;
    }
}

void set_leds(byte command, byte param)
{
    byte obj = get_param_obj(param);
    byte page = get_param_page(param);
    byte reset = get_param_reset(param);

    switch (command)
    {
        case CMD_FILL:
            set_color(obj, led.r, led.g, led.b, page);
            break;

        case CMD_CLEAR:
            set_color(obj, 0, 0, 0, page);
            break;
    }

    if (reset)
    {
        led.r = 0;
        led.g = 0;
        led.b = 0;
        log_led_status();
    }

    log_set_leds(command, obj, page, reset);
}

void fill(byte param)
{
    set_leds(CMD_FILL, param);
}

void clear(byte param)
{
    set_leds(CMD_CLEAR, param);
}

byte get_param_obj(byte param)
{
    return param & 3;
}

byte get_param_page(byte param)
{
    return (param >> 2) & 1;
}

byte get_param_reset(byte param)
{
    return (param >> 3) & 1;
}

void log_set(char name, byte value)
{
    sprintf(log_buffer, "set_%c(%d)", name, value);
    Serial.println(log_buffer);
    log_led_status();
}

void log_text(char *text)
{
    Serial.println(text);
}

void log_led_status()
{
    sprintf(log_buffer, "=> pos(%d, %d) rgb(%d, %d, %d)",
            led.x, led.y, led.r, led.g, led.b);
    Serial.println(log_buffer);
}

void log_set_leds(byte command, byte obj, byte page, byte reset)
{
    char *command_name;
    switch (command)
    {
        case CMD_FILL : command_name = "fill" ; break;
        case CMD_CLEAR: command_name = "clear"; break;
    }

    char *obj_name;
    switch (obj)
    {
        case PARAM_OBJ_LED: obj_name = "led"; break;
        case PARAM_OBJ_ROW: obj_name = "row"; break;
        case PARAM_OBJ_COL: obj_name = "col"; break;
        case PARAM_OBJ_ALL: obj_name = "all"; break;
    }

    char *page_name;
    switch (page)
    {
        case PARAM_PAGE_BG: page_name = "bg"; break;
        case PARAM_PAGE_FG: page_name = "fg"; break;
    }

    char *reset_name;
    switch (reset)
    {
        case PARAM_NORST: reset_name = "norst"; break;
        case PARAM_RESET: reset_name = "reset"; break;
    }

    sprintf(log_buffer, "%s(%s, %s, %s)",
            command_name, obj_name, page_name, reset_name);
    Serial.println(log_buffer);
}

void setup()
{
    Serial.begin(9600);
    Colorduino.Init();
    byte whiteBalVal[3] = {36, 63, 63};
    Colorduino.SetWhiteBal(whiteBalVal);
}

void loop()
{
    if (Serial.available())
    {
        byte data = Serial.read();
        byte command = data >> 4;
        byte param = data & 15;

        switch (command)
        {
            case CMD_SET_X: set_x(param); break;
            case CMD_SET_Y: set_y(param); break;

            case CMD_SET_R: set_r(param); break;
            case CMD_SET_G: set_g(param); break;
            case CMD_SET_B: set_b(param); break;

            case CMD_FLIP : flip_page() ; break;

            case CMD_FILL : fill(param) ; break;
            case CMD_CLEAR: clear(param); break;
        }
    }
}
