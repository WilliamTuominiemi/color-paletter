import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

img = Image.open("image4.jpg")
img = img.convert("RGB")

colors = img.getdata()

# Round colors so that similar colors are registered as the same
def round_color(color, precision=50):
    return tuple(int(round(c / precision) * precision) for c in color)


rounded_colors = [round_color(color) for color in colors]

color_counts = Counter(rounded_colors)

# Thresholds so that all colors that show too much or too little are ignored, makes a more unique palette
pixels = img.width * img.height
pick_scale = 20
threshold_min = (pixels / pick_scale) / 10
threshold_max = pixels / pick_scale

# Count how many colors there are left after thresholds have purged them
filtered_color_counts = {
    color: count
    for color, count in color_counts.items()
    if threshold_min < count < threshold_max
}

# Get the 7 most frequent colors from the purged list
top_colors = dict(
    sorted(filtered_color_counts.items(), key=lambda item: item[1], reverse=True)[:7]
)

# Create a canvas to display the result
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
