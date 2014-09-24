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
