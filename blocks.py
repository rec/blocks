"""

I have these four blocks each painted with four colors
in front of me that I want to fit into a frame such
that all four colors appear on all four sides.

Number the faces of a cube in front the viewer as follows:

  Side 0 is facing F
  Side 1 is under U
  Side 2 is right R
  Side 3 is above A
  Side 4 is to the left L
  Side 5 is the back B

This gives us four cubes:

  bgy yyr
  bgy rry
  bgy gbr
  bgg ryr

Note that the first cube is the only one with three of the same color.

In the frame, sides 2 and 4 are not visible.  We want to arrange the
four cubes we have so that all four colors appear on each side 0, 1, 3, 5.

We enumerate all possible permutations of the cube.

We start conceptually with side 0 facing, and
then cyclically permute sides (1, 2, 3, 4) - corresponding to rotating the
cube keeping the front facing us.

We then rotate so that another side is facing us.
We have to alternate two motions to do that:

Rotating Side 0 "up" - permuting (0, 1, 5, 3)
Rotating Side 0 "to the right" - permuting (0, 2, 5, 4)

"""

import itertools


def perms():
    def twist(f, u, r, a, l, b):
        return f, r, a, l, u, b

    def up(f, u, r, a, l, b):
        return u, b, r, f, l, a

    def right(f, u, r, a, l, b):
        return l, u, f, a, b, r

    result = []
    perm = tuple(range(6))
    for p1 in up, right, up, right, up, right:
        for p2 in twist, twist, twist, twist:
            result.append(perm)
            perm = p2(*perm)
        perm = p1(*perm)

    return result

PERMS = perms()
assert len(set(PERMS)) == 24


BLOCKS = 'bgyyyr', 'bgyrry', 'bgygbr', 'bggryr'


def permute_block(block, perms):
    return [''.join(block[i] for i in perm) for perm in perms]

BLOCK_PERMUTATIONS = [permute_block(b, PERMS) for b in BLOCKS]
assert all(len(p) == 24 for p in BLOCK_PERMUTATIONS)


def find():
    for perm in itertools.product(*BLOCK_PERMUTATIONS):
        f, u, _, a, _, b = [set(faces) == set('bgry') for faces in zip(*perm)]
        if f and u and a and b:
            print perm


if __name__ == '__main__':
    find()
