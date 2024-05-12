import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

img = Image.open("image4.jpg")
img = img.convert("RGB")

colors = img.getdata()


def round_color(color, precision=50):
    return tuple(int(round(c / precision) * precision) for c in color)


rounded_colors = [round_color(color) for color in colors]

color_counts = Counter(rounded_colors)

pixels = img.width * img.height
pick_scale = 20
threshold_min = (pixels / pick_scale) / 10
threshold_max = pixels / pick_scale

filtered_color_counts = {
    color: count
    for color, count in color_counts.items()
    if threshold_min < count < threshold_max
}

top_colors = dict(
    sorted(filtered_color_counts.items(), key=lambda item: item[1], reverse=True)[:7]
)


canvas_width = 800
canvas_height = 600
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

num_top_colors = len(top_colors)
bar_width = canvas_width // num_top_colors

x_position = 0
for color, count in top_colors.items():
    canvas[:, x_position : x_position + bar_width] = color
    x_position += bar_width

plt.imshow(canvas)
plt.axis("off")
plt.show()
