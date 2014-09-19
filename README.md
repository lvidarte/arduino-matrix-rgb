awesome-2048
============

Arduino Matrix RGB

Load Arduino Sketch
-------------------

First download Colorduino Interface Library for Arduino

    git clone https://github.com/lincomatic/Colorduino.git

Copy the lib to Arduino libraries dir

    sudo cp -r libraries/Colorduino /usr/share/arduino/libraries/

Then build and upload the Arduino sketch. I use [inotool](http://inotool.org) for that

   ino build && ino upload
