#!/usr/bin/python

from __future__ import print_function

"""
I have these four blocks each painted with four colors
in front of me that I want to fit into a frame such
that all four colors appear on all four sides.

Number the faces of a cube in front of the viewer as follows:

  Side 0 is facing F
  Side 1 is under U
  Side 2 is right R
  Side 3 is above A
  Side 4 is to the left L
  Side 5 is the back B

The four given cubes are then:

  bgy yyr
  bgy rry
  bgy gbr
  bgg ryr

All cubes have all four colors.
Note that the first cube is the only one with three faces with the same color.

In the frame, sides 2 and 4 are not visible.  We want to arrange the
four cubes we have so that all four colors appear on each side 0, 1, 3, 5.
"""

def rotations():
    """
    Return the rotational symmetry group of a cube.

    We keep the side 0 facing the viewer, and twist, rotating the
    sides (1, 2, 3, 4).

    We then rotate the cube so that another side is facing us and do it again.

    In order to reach all the sides that way, we need to alternate two motions:

        Rotating Side 0 "up" - permuting (0, 1, 5, 3)
        Rotating Side 0 "right" - permuting (0, 2, 5, 4)
    """

    def twist(f, u, r, a, l, b):
        return f, r, a, l, u, b

    def up(f, u, r, a, l, b):
        return u, b, r, f, l, a

    def right(f, u, r, a, l, b):
        return l, u, f, a, b, r

    def enumerate():
        perm = tuple(range(6))
        for p1 in up, right, up, right, up, right:
            for p2 in twist, twist, twist, twist:
                yield perm
                perm = p2(*perm)
            perm = p1(*perm)

    return tuple(enumerate())

ROTATIONS = rotations()
assert len(set(ROTATIONS)) == 24


# These are the actual blocks we have:
BLOCKS = 'bgyyyr', 'bgyrry', 'bgygbr', 'bggryr'


def rotate_blocks(blocks, rotations):
    def rotate_block(block):
        return tuple(''.join(block[i] for i in rot) for rot in rotations)

    return tuple(rotate_block(b) for b in blocks)

BLOCK_ROTATIONS = rotate_blocks(BLOCKS, ROTATIONS)


def find(rotations):
    results = []

    def add_block(i, blocks, ff, uu, bb, aa):
        for block in rotations[i]:
            f, u, _, a, _, b = block

            if not (f in ff or u in uu or b in bb or a in aa):
                bl = blocks + [block]
                if i >= len(rotations) - 1:
                    results.append(bl)
                else:
                    add_block(i + 1, bl, ff + f, uu + u, bb + b, aa + a)

    add_block(0, [], '', '', '', '')
    return results


if __name__ == '__main__':
    results = find(BLOCK_ROTATIONS)
    print('Number of results:', len(results))

    """
    Each unique result will appear as four rotations, each 90 degrees around
    the frame - and each rotation appears twice, rotated 180 degrees within the
    frame, reversing front and back and keeping the same faces hidden - so the
    number of unique results is 1/8 the number of total results.
    """

    print('Unique results:', len(results) / 8)
    for r in results:
        print(', '.join(r))
