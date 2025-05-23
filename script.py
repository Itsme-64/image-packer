from PIL import Image
import os

# --- Configuration ---
FOLDER = 'entity'           # Folder containing PNGs
MARGIN = 5                  # Margin between images
MAX_WIDTH = 512             # Max width of final image
OUTPUT_NAME = 'tiled_output.png'

# --- Load images ---
image_paths = [os.path.join(FOLDER, f) for f in os.listdir(FOLDER) if f.lower().endswith('.png')]
images = [Image.open(p).convert("RGBA") for p in image_paths]

# --- Placement algorithm ---
positions = []
x, y = 0, 0
row_max_height = 0

for img in images:
    w, h = img.size

    if x + w > MAX_WIDTH:
        x = 0
        y += row_max_height + MARGIN
        row_max_height = 0

    positions.append((img, (x, y)))
    x += w + MARGIN
    row_max_height = max(row_max_height, h)

final_height = y + row_max_height
output_image = Image.new("RGBA", (MAX_WIDTH, final_height), (255, 255, 255, 0))

for img, (x, y) in positions:
    output_image.paste(img, (x, y), img)

# --- Save ---
output_image.save(OUTPUT_NAME)
print(f"Saved tightly packed image as '{OUTPUT_NAME}'")