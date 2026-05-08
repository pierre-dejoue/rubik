Find the God's number of the 2x2x2 Rubik's cube
===============================================

Definition of the [God's number](https://en.wikipedia.org/wiki/God%27s_algorithm).

The convention used to describe a transformation of the cube (position and orientation of all corners) is the same as the one used in the Python script
in this repo. You can refer the the documentation of that script.

## Build

```
mkdir build
cd build
cmake -G "Visual Studio 17 2022" ..
cmake --build . --config Release
```

## Run

```
$ ./bin/Release/god_rubik2x2.exe
Find the God's number of the 2x2x2 Rubik's cube
[...]
Reachable configurations: 3674160
God's number: 11
```
