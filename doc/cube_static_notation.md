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

There are three possible orientations of a corner. To explain the naming convention used here, let's first observe that every corner has a colored face that is either down (D), or up (U) when the cube is in the solved state. Let's call that unique face the "star" face of that corner (*). With the Western color scheme, the * face is either the white or the yellow one.

The orientation of a corner is then:

- 0: The star face is either up or down (it is aligned with the XZ plane)
- 1: clockwise rotation from the 0 orientation
- 2: counterclockwise rotation from the 0 orientation

## Understand a static position

Let's see an example of a static position and decipher it. We'll use the script to generate the position after the moves "R U":

```
$ python rubik2x2.py -a "R U"
05124763:01200210
+---+-~-
cyclic_order: 15
```

### Position: 05124763

This is a permutation, noted _p_, of the solved position. The digit at index x infoms us about the current position of the original corner x. For example, the second digit tells us that corner 1 moved to position 5. Similarly for the other corners:

```
"Corner X moved to position Y = p(X)"

  X: 0 1 2 3 4 5 6 7
  Y: 0 5 1 2 4 7 6 3
```

Viewed that way, this is the [two-line notation](https://en.wikipedia.org/wiki/Permutation#Two-line_notation) of permutation _p_, of which we kept only the second line.

Notice that corners 0, 4 and 6 remained at their initial position.

Also notice that the other corners are permutated in a cycle of period 5: (57321)

### Orientations: 01200210

The orientation of all corners, indexed by their position of origin.

Going back to our discussion in the previous section: Corner 1 moved to position 5 due to the permutation. Looking at index 1 in the orientation array teaches us that corner 1 also has changed orientation by 1, i.e. a clockwise one-third rotation.

Another interesting example is corner 6, which stays at the same position, but change orientation. It has orientation 1, i.e. clockwise. One effect of the sequence of two moves "R U" is indeed to turn the corner 6 (the Right, Up, Front corner) in-place 120° clockwise.
