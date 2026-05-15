The 2x2x2 Cube Static Notation
==============================

This documentation is about the notation used by the script to describe a static position of the cube.

It is not about the standard move notation (aka the Singmaster notation) for which documentation is readily available.
A few links are provided below:

- [myrubik.com -- The 2x2x2 cube pieces and notation](https://myrubik.com/en/notation/2x2x2)
- [rubiks.fandom.com -- Notation](https://rubiks.fandom.com/wiki/Notation)

## Description of a position

In this program the cube's position is uniquely described by a colon-separated string, called a **static position**.
The first part corresponds to the position of the corners.
The second part corresponds to the orientation of the corners.

For example:
- The solved cube is represented by: `01234567:00000000`
- The cube after the two moves "R U" is represented by: `05124763:01200210`

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

The 8 corners can also be described with a three-letter string. Each letter corresponds to one of the three visible faces.
The letters are in the order of the X, Y, Z axis. For example the corner #3 can be written LUB, for Left, Up, Back.
The full correspondence is listed below:

  ```
  0: LDB
  1: RDB
  2: RUB
  3: LUB
  4: LDF
  5: RDF
  6: RUF
  7: LUF
  ```

## Orientation of the corners

There are three possible orientations of a corner. To explain the naming convention used here, let's first observe that
every corner has a colored face that is either down (D), or up (U) when the cube is in the solved state. Let's call that
unique face the "star" face of that corner (*). With the Western color scheme, the * face is either the white or the
yellow one.

The orientation of a corner is then:

- 0: The star face is either up or down (it is aligned with the XZ plane)
- 1: clockwise rotation from the 0 orientation
- 2: counterclockwise rotation from the 0 orientation

## Interpret a static position

Let's take the example of a static position and decipher it.
We'll use the script to generate the state of the cube after moves "R U":

  ```
  $  python rubik2x2.py -a "R U"
  05124763:01200210
  +---+-~-
  orientation_class: 0
  perm_cycles: (15732)(0)(4)(6)
  cyclic_order: 15
  ```

The **static position** `05124763:01200210` is composed of the position string `05124763` and
the orientation string `01200210`, that we will detail below.

### Positions: "05124763"

This is a permutation, noted _p_, of the solved position. The digit at index x infoms us about the current position of
the original corner x. For example, the second digit tells us that corner 1 moved to position 5. Similarly for the
other corners:

  ```
  "Corner X moved to position Y = p(X)"

    X: 0 1 2 3 4 5 6 7
    Y: 0 5 1 2 4 7 6 3
  ```

Viewed that way, this is the [two-line notation](https://en.wikipedia.org/wiki/Permutation#Two-line_notation)
of permutation _p_, of which we kept only the second line.

Notice that corners 0, 4 and 6 remained at their initial position.

Also notice that the other corners are permutated in a cycle of period 5: (15732)

### Orientations: "01200210"

The orientation of all corners, indexed by their position of origin.

In the previous section we identified that corner 1 has moved to position 5. Now, looking at index 1 in the
orientation list teaches us that corner 1 also has changed orientation by 1, i.e. a clockwise twist.

Another interesting example is corner 6, which stays at the same position, but change orientation. It has orientation
1, i.e. clockwise. Indeed, one effect of the sequence of two moves "R U" is to twist the corner 6 (the Right, Up,
Front corner) 120° clockwise.

## Write the static position of a physical cube

In order to write a static position, e.g. `05124763:01200210`, based on the state of a physical Rubik's cube,
follow the recipe:

- It will be helpful to have a color scheme defined, and to use the `--show-colors` option to obtain a description of
  the corners by their color.
- Go through the corners in order, from 0 to 7 (start with 0 'LDB', then 1 'RDB", etc.) and for each, find it on the
  physical cube:
  - The actual position of the corner (for instance, corner 1 moved to position **5**)
  - The orientation (for instance, corner 1 moved to position 5, and has orientation **1** (clockwise))
  - Append both values to the positions and orientations lists
- Once you're done, concatanate your 8-digit positions and orientations lists, separated by a colon ':'.
  This is the static description of the configuration. For example:
  - Positions list: `05124763`
  - Orientations list: `01200210`
  - The **static position**: `05124763:01200210`

## Cube patterns

Cube patterns are static descriptions of the cube that contain the wildcard character '*' (meaning "Any digit").
They can only be used with the `--search` option, to look for formulas that match that pattern.

For example, `01**45**:00**00**` is any cube position that leaves the down (D) layer, comprising of corners
[0, 1, 4, 5], invariant.

Unsurprisingly, all the up (U) rotations match that pattern:

  ```
  $ python rubik2x2.py -c 01**45**:00**00** --search
  Pivot: LDB (0)
  Recurse depth: 1
  01624573:00000000 1 [ U ]
  01764532:00000000 1 [ U2 ]
  01374526:00000000 1 [ U' ]
  ````
