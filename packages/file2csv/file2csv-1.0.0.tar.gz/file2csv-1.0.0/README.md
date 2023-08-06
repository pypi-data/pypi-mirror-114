# File2CSV

Project description Movement detector for RaspberryPi with Watch to watch objects coming into proximity. Pass pins Trigger and Echo. Pass offset to determine boundary for the object to come in

## Parse fixed width file

- Generates a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).
- Implements a parser that can parse the fixed width file and generate a delimited file, like CSV for example.

### Features

- Offset for object interference zone
- Emits Object In and Out event

### Installation

Create library
```console
python setup.py bdist_wheel
```


_RaspberryPiMovementDetector_ is a registered [PyPI module](https://pypi.python.org/pypi/RaspberryPiMovementDetector), so the installation
with _pip_ is quite easy:

```console
pip install RaspberryPiMovementDetector
```

## Examples

#### Basic usage

```python
import time
from RPi.GPIO import GPIO
from MovementDetector.Watch import Watch

TRIG = 23
ECHO = 24

def func_moved_in(arg):
  print("process for object entering field")

def func_moved_out(arg):
  print("process for object exiting field")

OFFSET = 200 # 2m

watch = Watch(gpio=GPIO, trig=TRIG, echo=ECHO, func_in=func_moved_in, func_out=func_moved_out, offset=OFFSET)

watch.observe()

time.sleep(100) # Sleep

watch.stop()
```

## Development

- Source hosted at [GitHub](https://github.com/KSanthanam/RaspberryPiMovementDetector)
- Python module hostet at [PyPI](https://pypi.python.org/pypi/RaspberryPiMovementDetector)
- Report issues, questions, feature requests on
  [GitHub Issues](https://github.com/KSanthanam/RaspberryPiMovementDetector/issues)

## License

The MIT License (MIT)

Copyright (c) 2019 KK Santhanam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Authors

KK Santhanam ([KSanthanam](https://github.com/KSanthanam))
