# Arduino Matrix RGB serial protocol for [ElecFreaks RGB Matrix Shield](http://www.elecfreaks.com/wiki/index.php?title=RGB_Matrix_Shield)

![ElecFreaks RGB Matrix Shield](https://github.com/lvidarte/arduino-matrix-rgb/blob/master/rgb-matrix.png)

### Load Arduino Sketch

First download Colorduino Interface Library for Arduino

    git clone https://github.com/lincomatic/Colorduino.git

Copy the lib to Arduino libraries dir

    sudo cp -r libraries/Colorduino /usr/share/arduino/libraries/

Then build and upload the Arduino sketch. I use [inotool](http://inotool.org) for that

    ino build && ino upload


### Test the matrix

Run matrix module in Shell mode

    $ matrix/shell.py /dev/ttyACM0

    Welcome to matrix shell
    Autocompletion and history are enabled

    Objects:
        serial    (object)  serial = Serial()
        matrix    (object)  matrix = Matrix(serial)
        demo      (object)  demo = Demo(matrix)

    Try the demo:
        demo.start()

    >>>

### Examples

Set red the led 0,0

```python
>>> matrix.set_pos(x=0, y=0)
>>> matrix.set_color(r=15, g=0, b=0)
>>> matrix.fill()
```

Set blue the led 1,1 in one step

```python
>>> matrix.set(x=1, y=1, r=0, g=0, b=15)
```

Showing actual state 

```python
>>> matrix
xy(1, 1) rgb(0, 0, 15) obj:led page:fg reset:off
```

Clear the actual page

```python
>>> matrix.clear_all()
```

Drawing in background page

```python
>>> matrix.set_page_bg()
>>> matrix.set_rand_color()
(9, 9, 14)
>>> matrix.set_rand_pos()
(6, 0)
>>> matrix
xy(6, 0) rgb(9, 9, 14) obj:led page:bg reset:off
>>> matrix.fill()
>>> matrix.flip()
```

Drawing a row of leds

```python
>>> matrix.set_obj_row()
>>> matrix.fill()
>>> matrix.flip()
```

Changing between pages

```python
>>> matrix.flip()
```

Reset the matrix to default values and draw a square

```python
>>> matrix.reset()
>>> matrix.set_rand_color()
(2, 6, 9)
>>> matrix.square(x=0, y=0, size=8)
```

### Little full example: forever random dots

```python
>>> import time
>>> while True
...   matrix.clear_all()
...   for i in range(10):
...      matrix.set_rand_all()
...      matrix.fill()
...      time.sleep(.5)
...
((7, 2), (2, 6, 0))
((7, 7), (12, 6, 10))
((4, 3), (4, 0, 7))
((1, 0), (5, 2, 8))
((7, 0), (13, 4, 13))
```

### Autocomplete and help

Just type matrix.[TAB][TAB] to see all methods

```python
>>> matrix.
matrix.b                  matrix.rect(
matrix.clear(             matrix.reset(
matrix.clear_all(         matrix.serial
matrix.clear_all_bg(      matrix.set(
matrix.clear_all_fg(      matrix.set0(
matrix.clear_col(         matrix.set_color(
matrix.clear_col_bg(      matrix.set_debug_off(
matrix.clear_col_fg(      matrix.set_debug_on(
matrix.clear_led(         matrix.set_obj_all(
matrix.clear_led_bg(      matrix.set_obj_col(
matrix.clear_led_fg(      matrix.set_obj_led(
matrix.clear_row(         matrix.set_obj_row(
matrix.clear_row_bg(      matrix.set_page_bg(
matrix.clear_row_fg(      matrix.set_page_fg(
matrix.fill(              matrix.set_pos(
matrix.fill_all(          matrix.set_rand_all(
matrix.fill_all_bg(       matrix.set_rand_color(
matrix.fill_all_fg(       matrix.set_rand_pos(
matrix.fill_col(          matrix.set_rand_rgb(
matrix.fill_col_bg(       matrix.set_rand_x(
matrix.fill_col_fg(       matrix.set_rand_xy(
matrix.fill_led(          matrix.set_rand_y(
matrix.fill_led_bg(       matrix.set_reset_off(
matrix.fill_led_fg(       matrix.set_reset_on(
matrix.fill_row(          matrix.set_rgb(
matrix.fill_row_bg(       matrix.set_rgb0(
matrix.fill_row_fg(       matrix.set_xy(
matrix.flip(              matrix.square(
matrix.g                  matrix.x
matrix.line_horizontal(   matrix.y
matrix.line_vertical(
matrix.r
```

Then use the help function

```python
>>> help(matrix.set0)

Help on method set0 in module matrix.matrix:

set0(self, x=0, y=0, r=0, g=0, b=0) method of matrix.matrix.Matrix instance
    Sets the state (xyrgb) and fill the actual object,
    0 by default
```

### Debug

Open a serial monitor for Arduino and set the debug on to enable verbosity

```python
>>> matrix.set_debug_on()
```
