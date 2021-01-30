from math import sqrt

mine_colors = [
    (233, 236, 236), #white
    (240, 118, 19),  #orange
    (189, 68, 179),  #magenta
    (58, 175, 217),  #light_blue
    (248, 198, 39),  #yellow
    (112, 185, 25),  #lime
    (237, 141, 172), #pink
    (62, 68, 71),    #dark_gray
    (142, 142, 134), #light_gray
    (21, 137, 145),  #cyan
    (121, 42, 172),  #purple
    (53, 57, 157),   #blue
    (114, 71, 40),   #brown
    (84, 109, 27),   #green
    (161, 39, 34),   #red
    (20, 21, 25),     #black
    (209, 177, 161),
    (159, 82, 36),
    (149, 87, 108),
    (112, 108, 138),
    (186, 133, 36),
    (103, 117, 53),
    (160, 77, 78),
    (57, 41, 35),
    (135, 107, 98),
    (87, 92, 92),
    (122, 73, 88),
    (76, 62, 92),
    (76, 50, 35),
    (76, 82, 42),
    (142, 60, 46),
    (37, 22, 16),
    (247, 233, 163)
]

def _square(x):
    return x * x


def cie94(L1_a1_b1, L2_a2_b2):
    """Calculate color difference by using CIE94 formulae

    See http://en.wikipedia.org/wiki/Color_difference or
    http://www.brucelindbloom.com/index.html?Eqn_DeltaE_CIE94.html.

    cie94(rgb2lab((255, 255, 255)), rgb2lab((0, 0, 0)))
    >>> 58.0
    cie94(rgb2lab(rgb(0xff0000)), rgb2lab(rgb('#ff0000')))
    >>> 0.0
    """

    L1, a1, b1 = L1_a1_b1
    L2, a2, b2 = L2_a2_b2

    C1 = sqrt(_square(a1) + _square(b1))
    C2 = sqrt(_square(a2) + _square(b2))
    delta_L = L1 - L2
    delta_C = C1 - C2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_H_square = _square(delta_a) + _square(delta_b) - _square(delta_C)
    return (sqrt(_square(delta_L)
                 + _square(delta_C) / _square(1.0 + 0.045 * C1)
                 + delta_H_square / _square(1.0 + 0.015 * C1)))


def rgb2lab(R_G_B):
    """Convert RGB colorspace to Lab

    Adapted from http://www.easyrgb.com/index.php?X=MATH.
    """

    R, G, B = R_G_B

    # Convert RGB to XYZ

    var_R = (R / 255.0)  # R from 0 to 255
    var_G = (G / 255.0)  # G from 0 to 255
    var_B = (B / 255.0)  # B from 0 to 255

    if (var_R > 0.04045):
        var_R = ((var_R + 0.055) / 1.055) ** 2.4
    else:
        var_R = var_R / 12.92
    if (var_G > 0.04045):
        var_G = ((var_G + 0.055) / 1.055) ** 2.4
    else:
        var_G = var_G / 12.92
    if (var_B > 0.04045):
        var_B = ((var_B + 0.055) / 1.055) ** 2.4
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100.0
    var_G = var_G * 100.0
    var_B = var_B * 100.0

    # Observer. = 2°, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    # Convert XYZ to L*a*b*

    var_X = X / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    var_Y = Y / 100.000  # ref_Y = 100.000
    var_Z = Z / 108.883  # ref_Z = 108.883

    if (var_X > 0.008856):
        var_X = var_X ** (1.0 / 3.0)
    else:
        var_X = (7.787 * var_X) + (16.0 / 116.0)
    if (var_Y > 0.008856):
        var_Y = var_Y ** (1.0 / 3.0)
    else:
        var_Y = (7.787 * var_Y) + (16.0 / 116.0)
    if (var_Z > 0.008856):
        var_Z = var_Z ** (1.0 / 3.0)
    else:
        var_Z = (7.787 * var_Z) + (16.0 / 116.0)

    CIE_L = (116.0 * var_Y) - 16.0
    CIE_a = 500.0 * (var_X - var_Y)
    CIE_b = 200.0 * (var_Y - var_Z)
    return (CIE_L, CIE_a, CIE_b)


def convert_rgb_to_minecraft_color_code(rgb):
    aux_index = -1
    min_dst = 999999999
    for index in range(len(mine_colors)):
        dst = cie94(rgb2lab(rgb), rgb2lab(mine_colors[index]))
        if min_dst > dst:
            min_dst = dst
            aux_index = index

    return aux_index

if __name__ == '__main__':

    with open("colors.binary", "wb") as file:
        for r in range(256):
           print(str((r)))
           for g in range(256):
               for b in range(256):
                   file.write((convert_rgb_to_minecraft_color_code((r, g, b))).to_bytes(1, byteorder='big'))