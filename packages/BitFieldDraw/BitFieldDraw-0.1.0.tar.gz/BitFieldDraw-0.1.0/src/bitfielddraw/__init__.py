"""BitFieldDraw
By Al Sweigart al@inventwithpython.com

A simple module for creating bit field art for strings or screens."""

__version__ = '0.1.0'


import shutil

TOP_BLOCK = chr(9600)
BOTTOM_BLOCK = chr(9604)
FULL_BLOCK = chr(9608)
EMPTY = ' '


def main():
    functions = [
        lambda x, y: (x ^ y) % 5,
        lambda x, y: (x ^ y) % 9,
        lambda x, y: (x ^ y) % 17,
        lambda x, y: (x ^ y) % 33,
        lambda x, y: (x ^ y) % 2,
        lambda x, y: (x ^ y) % 4,
        lambda x, y: (x ^ y) % 8,
        lambda x, y: (x | y) % 7,
        lambda x, y: (x | y) % 17,
        lambda x, y: (x | y) % 29,
        lambda x, y: (x * y) & 64,
        lambda x, y: (x * y) & 24,
        lambda x, y: (x * y) & 47,
        lambda x, y: (x ^ y) < 77,
        lambda x, y: (x ^ y) < 214,
        lambda x, y: (x ^ y) < 120,
        lambda x, y: (x * 2) % y,
        lambda x, y: (x * 64) % y,
        lambda x, y: (x * 31) % y,
        lambda x, y: ((x-128) * 64) % (y-128),
        lambda x, y: (x ^ y) & 32,
        lambda x, y: (x ^ y) & 72,
        lambda x, y: (x ^ y) & 23,
        lambda x, y: ((x * y) ** 4) % 7,
        lambda x, y: ((x * y) ** 5) % 99,
        lambda x, y: ((x * y) ** 9) % 3,
        lambda x, y: (x % y) % 4,
        lambda x, y: 40 % (x % y),
        lambda x, y: x & y,
        lambda x, y: x % y,
        lambda x, y: x & 9,
        lambda x, y: (x & y)   &   (x ^ y) % 19,
        lambda x, y: ((x ^ y) & 32)   *   ((x ^ y) % 9),
        lambda x, y: (x * 64) % y   *   ((x ^ y) < 77),
    ]

    for fn in functions:
        print(getBitFieldStr(fn, invertBit=True))
        input('Press Enter to continue...')


def getBitFieldDict(func, invertBit=False, left=0, top=None, width=None, height=None):
    WIDTH, HEIGHT = shutil.get_terminal_size()
    # We can't print to the last column on Windows without it adding a
    # newline automatically, so reduce the width by one:
    WIDTH -= 1
    HEIGHT *= 2  # We'll use squares for creating the height.

    if top is None:
        top = HEIGHT
    if width is None:
        width = WIDTH
    if height is None:
        height = HEIGHT

    canvas = {}
    for x in range(left, left + width):
        for y in range(top, top - height):
            canvas[(x, y)] = func(x, y)
    return canvas


def getBitFieldStrFromCanvas(canvas):
    pass


def getBitFieldImg(func, trueColor='white', falseColor='black'):
    import pillow
    pass

def saveBitFiledImg(filename, func, trueColor='white', falseColor='black'):
    pass

def getBitFieldStr(func, invertBit=False, left=0, top=None, width=None, height=None):
    WIDTH, HEIGHT = shutil.get_terminal_size()
    # We can't print to the last column on Windows without it adding a
    # newline automatically, so reduce the width by one:
    WIDTH -= 1
    HEIGHT *= 2  # We'll use squares for creating the height.

    if top is None:
        top = HEIGHT
    if width is None:
        width = WIDTH
    if height is None:
        height = HEIGHT

    rows = []
    for y in range(top, top - height, -2):
        row = []
        for x in range(left, left + width):
            try:
                top = func(x, y)  # top-half of text cell
            except:
                top = False

            if y - 1 <= top - height:
                bottom = False  # This bottom row should always be empty.
            else:
                try:
                    bottom = func(x, y - 1)  # bottom-half of text cell
                except:
                    bottom = False

            if invertBit:
                if top and bottom:
                    row.append(EMPTY)
                elif top and not bottom:
                    row.append(BOTTOM_BLOCK)
                elif not top and bottom:
                    row.append(TOP_BLOCK)
                else:
                    row.append(FULL_BLOCK)
            else:
                if top and bottom:
                    row.append(FULL_BLOCK)
                elif top and not bottom:
                    row.append(TOP_BLOCK)
                elif not top and bottom:
                    row.append(BOTTOM_BLOCK)
                else:
                    row.append(EMPTY)
        rows.append(''.join(row))
    return '\n'.join(rows)


def saveBitFieldStr(filename, func, invertBit=False, left=0, top=None, width=None, height=None):
    bitFieldStr = getBitFieldStr(func, invertBit, left, top, width, height)
    bitFieldFileObj = open(filename, 'w', encoding='utf-8')
    bitFieldFileObj.write(bitFieldStr)
    bitFieldFileObj.close()



if __name__ == '__main__':
    #main()
    saveBitFieldStr('out1.txt', lambda x, y: (x ^ y) % 5, invertBit=True, width=500, height=500)
