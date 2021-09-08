def format_color(r: int, g: int, b: int) -> str:
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def color_to_vector(color: list[int]) -> list[float]:
    mapper = lambda x: int(x, 16) / 256
    return [*map(mapper, [color[1:3], color[3:5], color[5:7]])]
