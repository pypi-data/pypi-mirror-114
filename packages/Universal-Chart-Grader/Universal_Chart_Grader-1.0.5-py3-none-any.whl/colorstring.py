#!/usr/local/bin/python3
"""
Color String
Easily create colored strings that behave like str in Python 3.

This package comes from https://github.com/simonsolnes/colorstring all credit goes to the original author
License: GPLv3 https://github.com/simonsolnes/colorstring/blob/master/LICENSE
"""

import copy
import re

colors = {color: idx for idx, color in enumerate([
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'normal',
    'primary'
])}

formats = {frmt: idx for idx, frmt in enumerate([
    'normal',
    'bold',
    'faint',
    'italic',
    'underline',
    'slowblink',
    'rapidblink',
    'negative',
    'conceal',
    'crossedout',
    'primary'])}

ansi = 'ansi'
rgb = 'rgb'


class ColorPart():
    pre = '\x1b['
    post = '\x1b[0m'

    def __init__(self, text='', frmt='primary', fg='primary', bg='primary'):
        self.text = text

        if isinstance(frmt, list):
            for f in frmt[:-1]:
                self.text = ColorPart(self.text, f)
            self.frmt = frmt[-1]
        else:
            self.frmt = frmt

        if isinstance(fg, tuple):
            self.text = self.text
            self.frmt = rgb

        self.fg = fg

        self.bg = bg

    def __str__(self):
        if self.frmt == rgb:
            fg = ';'.join((str(i) for i in self.fg))
            return self.pre + '38;2;' + fg + 'm' + str(self.text) + self.post
        else:
            fg = str(self.fg)
            bg = str(self.bg)
            frmt = str(self.frmt)
            return self.pre + frmt + ';' + fg + ';' + bg + 'm' + str(self.text) + self.post

    @property
    def fg(self):
        return self._fg

    @fg.setter
    def fg(self, x):
        if isinstance(x, int):
            if x < 39 and x > 29:
                self._fg = x
            else:
                self._fg = 30 + x
        elif isinstance(x, tuple):
            assert (all((i < 256 and i >= 0 for i in x)) and len(x) == 3)
            self._fg = x
        else:
            assert (x in colors)
            self._fg = 30 + colors[x]

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, x):
        if isinstance(x, int):
            if x < 49 and x > 39:
                self._bg = x
            else:
                self._bg = 40 + x
        else:
            assert (x in colors)
            self._bg = 40 + colors[x]

    @property
    def frmt(self):
        return self._frmt

    @frmt.setter
    def frmt(self, x):
        if isinstance(x, int):
            self._frmt = x
        elif x == rgb:
            self._frmt = rgb
        else:
            assert (x in formats)
            self._frmt = formats[x]


class Color():
    def __init__(self, text='', frmt='primary', fg='primary', bg='primary'):
        if isinstance(text, int):
            text = str(text)
        self.parts = [ColorPart(text, frmt, fg, bg)]

    def separated(self):
        separated = []
        for part in self.parts:
            for ch in part.text:
                separated.append(ColorPart(ch, part.frmt, part.fg, part.bg))
        return separated

    def cohesed(self):
        cohesed = []
        for part in self.parts:
            if len(cohesed) == 0:
                cohesed.append(part)
                continue
            last = cohesed[-1]
            if cohesed and part.fg == last.fg and part.bg == last.bg and part.frmt == last.frmt:
                last.text += part.text
            else:
                cohesed.append(part)

        return list(filter(lambda x: x.text, cohesed))

    def __str__(self):
        # return self.__repr__()
        return ''.join([str(i) for i in self.parts])

    def __repr__(self):
        return ''.join([i.text for i in self.parts])

    def __add__(self, x):
        if isinstance(x, Color):
            self.parts += x.parts
        elif isinstance(x, str):
            self.parts.append(ColorPart(x))
        else:
            raise TypeError('Requires either Color or str')
        return self

    def __radd__(self, x):
        if isinstance(x, Color):
            self.parts = x.parts + self.parts
        elif isinstance(x, str):
            self.parts.insert(0, ColorPart(x))
        else:
            raise TypeError('Requires either Color or str')
        return self

    def __len__(self):
        return sum([len(part.text) for part in self.parts])

    def __getitem__(self, key):
        filtered = self.separated()[key]
        ret = Color()
        ret.parts = [filtered] if not isinstance(filtered, list) else filtered
        ret.parts = ret.cohesed()
        return ret

    def __hash__(self):
        return hash(str(self))

    def rjust(self, width, fillchar=' '):
        if len(self) >= width:
            return self
        return Color((width - len(self)) * fillchar) + self

    def ljust(self, width, fillchar=' '):
        if len(self) >= width:
            return self
        return self + Color((width - len(self)) * fillchar)

    def center(self, width, fillchar=' '):
        if len(self) >= width:
            return self
        pad = width - len(self)
        right = left = int(pad / 2)
        if pad % 2 != 0:
            right += 1
        return Color(left * fillchar) + self + Color(right * fillchar)

    def replace(self, old, new):
        new_s = copy.deepcopy(self)
        for i in range(len(new_s.parts)):
            new_s.parts[i].text = new_s.parts[i].text.replace(old, new)
        return new_s


def test():
    teststrings = [

        # Argument usage

        'keywords',
        Color('fish', frmt='italic', fg='red', bg='yellow'),
        'positional',
        Color('fish', 'bold', 'blue', 'normal'),
        'only frmt',
        Color('fish', 'faint'),
        'numbers',
        Color('fish', fg=1),
        'several formats (not colors)',
        Color('fish', ['italic', 'bold', 'faint', 'underline'], 'red'),
        'rgb',
        Color('fish', fg=(0, 255, 0)),
        'rgb2',
        Color(Color('fish', fg=(0, 255, 0)), 'bold'),
        'rgb3',
        Color(Color('fish', 'bold'), fg=(255, 0, 0)),
        'rgb4 this has a bug',
        Color(Color('fish'), fg=(255, 0, 0)),

        # Features

        'len',
        str(len(Color('this string has a length of 30', 'bold'))),
        'addition',
        Color('one', fg='red') + Color('two', fg='blue'),
        'indexing',
        (Color('one', fg='red') + Color('two', fg='blue'))[2],
        'splice',
        (Color('one', fg='red') + Color('two', fg='blue'))[2:5],
        'splice 2',
        (Color('oioi', fg='red') + Color('apap', fg='blue'))[::2],
        'nested strings',
        Color(Color('s') + Color(Color('s') + Color('s'))),
        'length of nested strings works',
        str(len(Color(Color('s') + Color(Color(Color('ss', 'faint'), 'bold') + Color('s'), 'italic')))),

        'rjust',
        Color('fish', frmt='italic', fg='red', bg='yellow').rjust(30),
        'ljust',
        Color('fish', frmt='italic', fg='red', bg='yellow').ljust(30, '-'),
        'center',
        Color('fi', frmt='italic', fg='red', bg='yellow').center(5, '-'),

    ]

    for test in zip(teststrings[::2], teststrings[1::2]):
        print(test[0])
        print(Color('\t') + test[1])


def remove_color(s: str):
    new_str, _ = re.subn(r"\x1b\[(?:\d+;?)*m", "", s)
    return new_str


if __name__ == '__main__':
    test()
