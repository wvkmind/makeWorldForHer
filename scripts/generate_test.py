"""Test: generate a character sprite via ComfyUI API."""
from comfyui_api import text_to_image, download_image

prompt = (
    "masterpiece, best quality, ultra-detailed, anime style, cel-shaded, "
    "1girl, solo, young woman, age 18, 160cm, "
    "long dual-ponytail hair, pink to purple gradient hair, side bangs, "
    "large expressive eyes, purple-blue iris, fair skin, pink blush, "
    "delicate features, sweet smile expression, "
    "slender figure, medium breasts, long legs, "
    "wearing fitted black crop top and white pleated mini skirt, "
    "standing pose, full body, facing viewer, "
    "solid bright green background, green screen, chroma key green background, "
    "clean lineart, soft shading, "
    "modern anime illustration style, light novel cover quality, "
    "normal human proportions, NOT chibi, NOT super deformed"
)

print(f"Generating with prompt: {prompt[:80]}...")
pid, images = text_to_image(prompt, width=768, height=1024)

for img in images:
    out_path = f"xiaoai_app/assets/sprites/character/standing_smile.png"
    download_image(img["filename"], img["subfolder"], out_path)
    print(f"Done! Saved to {out_path}")
