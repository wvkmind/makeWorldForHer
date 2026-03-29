"""Remove green screen background using chroma key."""
from PIL import Image
import numpy as np

input_path = "xiaoai_app/assets/sprites/character/standing_smile.png"
output_path = "xiaoai_app/assets/sprites/character/standing_smile_cutout.png"

img = Image.open(input_path).convert("RGBA")
data = np.array(img, dtype=np.float32)
print(f"Input: {img.size}")

r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

# Green screen detection: green channel dominant
green_mask = (g > 100) & (g > r * 1.3) & (g > b * 1.3)

# Soft edge: calculate how "green" each pixel is
green_strength = np.clip((g - np.maximum(r, b)) / 80.0, 0, 1)
alpha = np.where(green_mask, (1.0 - green_strength) * 255, 255).astype(np.uint8)

result_data = np.array(img)
result_data[:,:,3] = alpha

# Despill: remove green tint from edge pixels
edge_mask = (alpha > 0) & (alpha < 250)
if np.any(edge_mask):
    # Reduce green channel on semi-transparent pixels
    max_rb = np.maximum(result_data[:,:,0], result_data[:,:,2])
    result_data[:,:,1] = np.where(edge_mask, np.minimum(result_data[:,:,1], max_rb), result_data[:,:,1])

# Also despill fully opaque pixels near edges (dilate edge mask by 2px)
from scipy.ndimage import binary_dilation
edge_dilated = binary_dilation(edge_mask, iterations=2)
opaque_near_edge = edge_dilated & (alpha == 255)
if np.any(opaque_near_edge):
    max_rb2 = np.maximum(result_data[:,:,0], result_data[:,:,2])
    excess_green = result_data[:,:,1].astype(np.int16) - max_rb2.astype(np.int16)
    excess_green = np.clip(excess_green, 0, 255).astype(np.uint8)
    result_data[:,:,1] = np.where(opaque_near_edge, 
        result_data[:,:,1] - (excess_green * 0.7).astype(np.uint8), 
        result_data[:,:,1])

result = Image.fromarray(result_data)

# Crop to content (remove empty space)
bbox = result.getbbox()
if bbox:
    result = result.crop(bbox)
    print(f"Cropped to: {result.size}")

result.save(output_path)
print(f"Saved to {output_path}")
