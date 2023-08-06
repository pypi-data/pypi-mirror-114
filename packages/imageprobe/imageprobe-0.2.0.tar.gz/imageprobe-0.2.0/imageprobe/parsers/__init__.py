from imageprobe.parsers import gif, png

# Parsers are ordered from the ones that require the least amount of data onwards.
ordered_parsers = [
    gif.gif,  # 10 bytes
    png.png,  # 24 bytes
]
