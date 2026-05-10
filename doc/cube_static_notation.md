The 2x2x2 Cube Static Notation
==============================

This documentation is about the notation used by the script to describe a static position of the cube.

It is not about the standard move notation (aka the Singmaster notation) for which documentation is readily available. A few links are provided below:

- [myrubik.com -- The 2x2x2 cube pieces and notation](https://myrubik.com/en/notation/2x2x2)
- [rubiks.fandom.com -- Notation](https://rubiks.fandom.com/wiki/Notation)

## Description of a position

In this program the cube's position is uniquely described by a colon-separated string. The first
part corresponds to the position of the corners. The second part corresponds to the orientation of the corners.

For example, the solved cube is represented by: `1234567:00000000`

## Position of the corners

The 8 corners of the cube are identified as follows:

```
    Back layer (B):

      3   2

      0   1

    Front layer (F):

      7   6

      4   5
```

## Orientation of the corners

There are three possible orientations of a corner. To explain the naming convention used here, let's first observe that every corner has a colored face that is either down (D), or up (U) when the cube is in the solved state. Let's call that unique face the star face of the corner (*).

The orientation of a corner is then:

- 0: The star face is either up or down (it is aligned with the XZ plane)
- 1: clockwise rotation from the 0 orientation
- 2: counterclockwise rotation from the 0 orientation

## Understand a static position

Let's see an example of a static position and decipher it. We'll use the script to generate the position after the moves "R B":

```
$ python rubik2x2.py -a "R B"
15204637:11120220
--~-+--+
cyclic_order: 15
```

### Position: 15204637

This is a permutation of the solved position. The digit at index x infoms us about the current position of the original corner x. For example, the first digit tells us that corner 0 moved to position 1. Similarly:

```
"Corner X moved to position Y"

X -> Y
0 -> 1
1 -> 5
2 -> 2
3 -> 0
4 -> 4
5 -> 6
6 -> 3
7 -> 7
```

Notice that corners 2, 4 and 7 remained at their initial position.

### Orientations: 11120220

TBD
