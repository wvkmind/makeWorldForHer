"""Full pipeline test:
1. Text2Img: generate empty living room background
2. Text2Img: generate character with green screen
3. Cutout: remove green background
4. Image Edit (2 img): combine background + character reference -> integrated scene
"""
from comfyui_api import text_to_image, image_edit_2, cutout_green, download_image

OUT = "xiaoai_app/assets"

# --- Step 1: Generate empty room background ---
print("\n=== Step 1: Generate living room background ===")
bg_prompt = (
    "anime style interior illustration, cozy living room, "
    "warm lighting, sofa on the left, TV on the right wall, "
    "desk near window, pink and white color scheme, "
    "afternoon sunlight through window, no people, empty room, "
    "detailed background, high quality, modern anime style"
)
pid, imgs = text_to_image(bg_prompt, width=1024, height=768, prefix="bg_living")
bg_path = f"{OUT}/backgrounds/bg_living_room.png"
download_image(imgs[0]["filename"], imgs[0]["subfolder"], bg_path)

# --- Step 2: Generate character with green screen ---
print("\n=== Step 2: Generate character (green screen) ===")
char_prompt = (
    "masterpiece, best quality, ultra-detailed, anime style, cel-shaded, "
    "1girl, solo, young woman, age 18, 160cm, "
    "long dual-ponytail hair, pink to purple gradient hair, side bangs, "
    "large expressive eyes, purple-blue iris, fair skin, pink blush, "
    "sweet smile, slender figure, long legs, "
    "wearing fitted black crop top and white pleated mini skirt, "
    "standing pose, full body, facing viewer, feet visible, "
    "solid bright green background, green screen, chroma key, "
    "normal human proportions, NOT chibi"
)
pid, imgs = text_to_image(char_prompt, width=768, height=1152, prefix="char_standing")
char_raw = f"{OUT}/sprites/character/standing_smile_raw.png"
download_image(imgs[0]["filename"], imgs[0]["subfolder"], char_raw)

# --- Step 3: Cutout green screen ---
print("\n=== Step 3: Cutout green screen ===")
char_cutout = f"{OUT}/sprites/character/standing_smile.png"
cutout_green(char_raw, char_cutout)

# --- Step 4: Image edit - put character in room ---
print("\n=== Step 4: Generate integrated scene (character in room) ===")
edit_prompt = (
    "将第二张图中的粉紫双马尾少女放入第一张图的客厅中，"
    "她坐在沙发上，微笑着，光影和风格与背景一致"
)
pid, imgs = image_edit_2(bg_path, char_cutout, edit_prompt, prefix="scene_living")
scene_path = f"{OUT}/scenes/living_room_sitting_smile.png"
download_image(imgs[0]["filename"], imgs[0]["subfolder"], scene_path)

print("\n=== Done! ===")
print(f"Background:  {bg_path}")
print(f"Character:   {char_cutout}")
print(f"Scene:       {scene_path}")
