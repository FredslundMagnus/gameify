from __future__ import annotations


class Transparent:
    def __init__(self, r: int, g: int, b: int, alpha: int) -> None:
        self.color: tuple[int, int, int, int] = (r, g, b, alpha)


class Color:
    def __init__(self, r: int, g: int, b: int) -> None:
        self.color: tuple[int, int, int] = (r, g, b)

    def transparrent(self, alpha=255):
        r, g, b = self.color
        return Transparent(r, g, b, alpha)

    @staticmethod
    def interpolate(color1: Color, color2: Color, x: float) -> Color:
        # Should convert RGB to HSV
        return Color(*(int((v2 - v1)*x+v1) for v1, v2 in zip(color1.color, color2.color)))


class MaterialColor(Color):
    def __init__(self, c50: Color, c100: Color, c200: Color, c300: Color, c400: Color, c500: Color, c600: Color, c700: Color, c800: Color, c900: Color) -> None:
        self.c50:  Color = c50
        self.c100: Color = c100
        self.c200: Color = c200
        self.c300: Color = c300
        self.c400: Color = c400
        self.c500: Color = c500
        self.c600: Color = c600
        self.c700: Color = c700
        self.c800: Color = c800
        self.c900: Color = c900
        self.color: tuple[int, int, int] = c500.color
        # self.r, self.g, self.b, self.a = c500.r, c500.g, c500.b, c500.a,
        self.table: dict[int, Color] = {50: c50, 100: c100, 200: c200, 300: c300, 400: c400, 500: c500, 600: c600, 700: c700, 800: c800, 900: c900}

    def __getitem__(self, index: int) -> Color:
        return self.table[index]


class Colors:
    red: MaterialColor = MaterialColor(Color(255, 235, 238), Color(255, 205, 210), Color(239, 154, 154), Color(229, 115, 115), Color(239, 83, 80), Color(244, 67, 54), Color(229, 57, 53), Color(211, 47, 47), Color(198, 40, 40), Color(183, 28, 28))
    pink: MaterialColor = MaterialColor(Color(252, 228, 236), Color(248, 187, 208), Color(244, 143, 177), Color(240, 98, 146), Color(236, 64, 122), Color(233, 30, 99), Color(216, 27, 96), Color(194, 24, 91), Color(173, 20, 87), Color(136, 14, 79))
    purple: MaterialColor = MaterialColor(Color(243, 229, 245), Color(225, 190, 231), Color(206, 147, 216), Color(186, 104, 200), Color(171, 71, 188), Color(156, 39, 176), Color(142, 36, 170), Color(123, 31, 162), Color(106, 27, 154), Color(74, 20, 140))
    deepPurple: MaterialColor = MaterialColor(Color(237, 231, 246), Color(209, 196, 233), Color(179, 157, 219), Color(149, 117, 205), Color(126, 87, 194), Color(103, 58, 183), Color(94, 53, 177), Color(81, 45, 168), Color(69, 39, 160), Color(49, 27, 146))
    indigo: MaterialColor = MaterialColor(Color(232, 234, 246), Color(197, 202, 233), Color(159, 168, 218), Color(121, 134, 203), Color(92, 107, 192), Color(63, 81, 181), Color(57, 73, 171), Color(48, 63, 159), Color(40, 53, 147), Color(26, 35, 126))
    blue: MaterialColor = MaterialColor(Color(227, 242, 253), Color(187, 222, 251), Color(144, 202, 249), Color(100, 181, 246), Color(66, 165, 245), Color(33, 150, 243), Color(30, 136, 229), Color(25, 118, 210), Color(21, 101, 192), Color(13, 71, 161))
    lightBlue: MaterialColor = MaterialColor(Color(225, 245, 254), Color(179, 229, 252), Color(129, 212, 250), Color(79, 195, 247), Color(41, 182, 246), Color(3, 169, 244), Color(3, 155, 229), Color(2, 136, 209), Color(2, 119, 189), Color(1, 87, 155))
    cyan: MaterialColor = MaterialColor(Color(224, 247, 250), Color(178, 235, 242), Color(128, 222, 234), Color(77, 208, 225), Color(38, 198, 218), Color(0, 188, 212), Color(0, 172, 193), Color(0, 151, 167), Color(0, 131, 143), Color(0, 96, 100))
    teal: MaterialColor = MaterialColor(Color(224, 242, 241), Color(178, 223, 219), Color(128, 203, 196), Color(77, 182, 172), Color(38, 166, 154), Color(0, 150, 136), Color(0, 137, 123), Color(0, 121, 107), Color(0, 105, 92), Color(0, 77, 64))
    green: MaterialColor = MaterialColor(Color(232, 245, 233), Color(200, 230, 201), Color(165, 214, 167), Color(129, 199, 132), Color(102, 187, 106), Color(76, 175, 80), Color(67, 160, 71), Color(56, 142, 60), Color(46, 125, 50), Color(27, 94, 32))
    lightGreen: MaterialColor = MaterialColor(Color(241, 248, 233), Color(220, 237, 200), Color(197, 225, 165), Color(174, 213, 129), Color(156, 204, 101), Color(139, 195, 74), Color(124, 179, 66), Color(104, 159, 56), Color(85, 139, 47), Color(51, 105, 30))
    lime: MaterialColor = MaterialColor(Color(249, 251, 231), Color(240, 244, 195), Color(230, 238, 156), Color(220, 231, 117), Color(212, 225, 87), Color(205, 220, 57), Color(192, 202, 51), Color(175, 180, 43), Color(158, 157, 36), Color(130, 119, 23))
    yellow: MaterialColor = MaterialColor(Color(255, 253, 231), Color(255, 249, 196), Color(255, 245, 157), Color(255, 241, 118), Color(255, 238, 88), Color(255, 235, 59), Color(253, 216, 53), Color(251, 192, 45), Color(249, 168, 37), Color(245, 127, 23))
    amber: MaterialColor = MaterialColor(Color(255, 248, 225), Color(255, 236, 179), Color(255, 224, 130), Color(255, 213, 79), Color(255, 202, 40), Color(255, 193, 7), Color(255, 179, 0), Color(255, 160, 0), Color(255, 143, 0), Color(255, 111, 0))
    orange: MaterialColor = MaterialColor(Color(255, 243, 224), Color(255, 224, 178), Color(255, 204, 128), Color(255, 183, 77), Color(255, 167, 38), Color(255, 152, 0), Color(251, 140, 0), Color(245, 124, 0), Color(239, 108, 0), Color(230, 81, 0))
    deepOrange: MaterialColor = MaterialColor(Color(251, 233, 231), Color(255, 204, 188), Color(255, 171, 145), Color(255, 138, 101), Color(255, 112, 67), Color(255, 87, 34), Color(244, 81, 30), Color(230, 74, 25), Color(216, 67, 21), Color(191, 54, 12))
    brown: MaterialColor = MaterialColor(Color(239, 235, 233), Color(215, 204, 200), Color(188, 170, 164), Color(161, 136, 127), Color(141, 110, 99), Color(121, 85, 72), Color(109, 76, 65), Color(93, 64, 55), Color(78, 52, 46), Color(62, 39, 35))
    gray: MaterialColor = MaterialColor(Color(250, 250, 250), Color(245, 245, 245), Color(238, 238, 238), Color(224, 224, 224), Color(189, 189, 189), Color(158, 158, 158), Color(117, 117, 117), Color(97, 97, 97), Color(66, 66, 66), Color(33, 33, 33))
    blueGray: MaterialColor = MaterialColor(Color(236, 239, 241), Color(207, 216, 220), Color(176, 190, 197), Color(144, 164, 174), Color(120, 144, 156), Color(96, 125, 139), Color(84, 110, 122), Color(69, 90, 100), Color(55, 71, 79), Color(38, 50, 56))
    black: Color = Color(0, 0, 0)
    white: Color = Color(255, 255, 255)
