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
