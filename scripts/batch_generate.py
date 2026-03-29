"""Batch generate all images. Usage: python scripts/batch_generate.py [category]
Categories: bg, sprite_home, sprite_out, scene_lr, scene_br, scene_kt, scene_bt, scene_bl, all
"""
import sys, os
from comfyui_api import text_to_image, image_edit_2, image_edit_1, cutout_green, download_image

OUT = os.path.join(os.path.dirname(__file__), "..", "xiaoai_app", "assets")

# ============================================================
# Resolution settings
# ============================================================
BG_W, BG_H = 1024, 768       # 背景：宽幅横图
SPRITE_W, SPRITE_H = 768, 1152  # 绿幕立绘：竖长图
SCENE_W, SCENE_H = 1024, 768   # 一体图：宽幅横图（和背景一致）

# ============================================================
# Character identity (from id.md) - NEVER change these
# ============================================================
CHAR_ID = (
    "1girl, solo, beautiful young woman, age 18, 165cm tall, "
    "long dual-ponytail hair with gradient from soft pink to lavender purple, "
    "flowing past waist, side-swept bangs with face-framing strands, "
    "silky slightly wavy hair ends, "
    "large expressive anime eyes with purple-blue gradient irises and light reflections, "
    "long eyelashes, small pointed nose, soft pink lips with slight pout, "
    "fair porcelain skin with natural blush on cheeks, delicate beautiful features, "
    "slender figure, medium bust, long slender legs, small waist, petite hands, "
    "tall and elegant proportions"
)

STYLE = (
    "masterpiece, best quality, ultra-detailed, anime style, cel-shaded, "
    "vibrant colors, clean lineart, soft shading, "
    "modern anime illustration style, light novel cover quality, "
    "normal human proportions, NOT chibi, NOT super deformed"
)

# ============================================================
# Expressions (from id.md)
# ============================================================
EXPR = {
    "smile": "gentle closed-mouth smile, slight blush, soft eyes",
    "laugh": "open mouth laughing, eyes squinted into happy arcs",
    "neutral": "calm gaze, slight smile, relaxed posture",
    "shy": "looking away, heavy blush, fingers touching together",
    "sleepy": "half-lidded eyes, slight yawn, rubbing one eye",
    "focused": "slightly furrowed brows, concentrated gaze",
    "excited": "eyes sparkling, big smile, energetic",
    "pout": "puffed cheeks, eyebrows slightly furrowed, looking to side",
    "surprised": "eyes wide open, mouth small o shape, one hand near mouth",
}

# ============================================================
# Outfits
# ============================================================
HOME_OUTFITS = {
    "H01": "oversized pastel pink hoodie covering hands, white shorts barely visible under hoodie, barefoot",
    "H02": "black lace-trim camisole, pink cotton shorts, barefoot",
    "H03": "loose white t-shirt, grey sweatpants, barefoot",
    "H04": "purple satin nightgown knee length, thin straps, barefoot",
    "H05": "pink pajama set with button-up top and matching pants, barefoot",
    "H06": "navy and white striped long sleeve shirt, denim shorts, barefoot",
    "H07": "fitted black crop top showing hint of midriff, white pleated mini skirt, barefoot",
    "H08": "lavender knit cardigan over white tank top, shorts, barefoot",
    "H09": "pink sports bra and black athletic shorts, barefoot",
    "H10": "wrapped in large pink bath towel, wet hair down, barefoot",
}

OUT_OUTFITS = {
    "O01": "white button-up blouse with puff sleeves, pink A-line mini skirt, white ribbon choker, white mary janes",
    "O02": "black sleeveless fitted dress knee length, thin belt, heeled sandals",
    "O03": "light blue denim jacket over white t-shirt, blue jeans, white sneakers",
    "O04": "pink floral sundress with thin straps, straw hat, brown sandals",
    "O05": "pastel pink tracksuit zip-up jacket and pants, white sneakers",
    "O06": "japanese sailor school uniform, navy blue pleated skirt, white top with navy collar, red ribbon tie",
    "O07": "white puffy winter jacket, pink knit scarf, black tights, brown fur-lined boots",
    "O08": "red plaid flannel shirt tied at waist, black high-waisted mini skirt, black ankle boots",
    "O09": "light floral spaghetti strap midi dress, wide-brim sun hat, woven sandals, summer",
    "O10": "oversized beige blazer, white crop top, black shorts, black heels, cool casual style",
}

# ============================================================
# Room backgrounds (from world-design.md - exact details)
# ============================================================
BACKGROUNDS = {
    "living_room_day": (
        "anime style interior illustration, cozy living room 18sqm, "
        "warm white walls, wood floor, pink and purple ambient LED strip along wall edges, "
        "LEFT SIDE: cream-white fabric 3-seat sofa with 3 throw pillows (1 pink, 1 purple, 1 bear-shaped), "
        "white round coffee table in front with TV remote and pink mug and tissue box, "
        "light grey fluffy carpet between sofa and table, large brown teddy bear on sofa corner, "
        "RIGHT SIDE: white low TV cabinet 1.5m long, 55-inch black TV on cabinet, "
        "Nintendo Switch with 2 controllers on cabinet, "
        "3 small framed paintings above TV (starry sky, cat, flowers), warm yellow fairy lights along top edge, "
        "WINDOW CORNER: white simple desk 1.2m with pink MacBook laptop with stickers, "
        "24-inch white monitor, pink mechanical keyboard, white wireless mouse, "
        "pink cat-paw mug with tea, white pen holder, warm desk lamp, "
        "small white 3-tier bookshelf beside desk with books, "
        "two small succulents on windowsill (one green one purple), "
        "south-facing large window with white sheer curtains and light purple blackout curtains, "
        "bright afternoon warm sunlight streaming in, daytime, "
        "no people, empty room, high quality, detailed"
    ),
    "living_room_night": (
        "anime style interior illustration, cozy living room 18sqm, nighttime, "
        "warm white walls, wood floor, pink and purple ambient LED strip glowing along wall edges, "
        "LEFT SIDE: cream-white fabric 3-seat sofa with 3 throw pillows (1 pink, 1 purple, 1 bear-shaped), "
        "white round coffee table in front with TV remote and pink mug and tissue box, "
        "light grey fluffy carpet between sofa and table, large brown teddy bear on sofa corner, "
        "RIGHT SIDE: white low TV cabinet 1.5m long, 55-inch black TV on cabinet, "
        "Nintendo Switch with 2 controllers on cabinet, "
        "3 small framed paintings above TV (starry sky, cat, flowers), warm yellow fairy lights glowing along top edge, "
        "WINDOW CORNER: white simple desk 1.2m with pink MacBook laptop with stickers, "
        "24-inch white monitor, pink mechanical keyboard, white wireless mouse, "
        "pink cat-paw mug with tea, white pen holder, warm desk lamp turned on, "
        "small white 3-tier bookshelf beside desk with books, "
        "south-facing large window showing dark night sky with city lights, curtains partially open, "
        "warm indoor lighting, ceiling light on, ambient LED glow, cozy night atmosphere, "
        "no people, empty room, high quality, detailed"
    ),
    "bedroom_day": (
        "anime style interior illustration, cozy bedroom 14sqm, daytime, "
        "pink-purple color scheme walls, "
        "glow-in-dark star stickers on wall, "
        "CENTER: 1.5m double bed with white wooden frame, light purple bedsheets, white duvet, 2 pillows, "
        "5-6 plush toys on bed against wall (rabbit, cat, hamster, small dinosaur, shiba inu), "
        "LEFT: white bedside table with moon-shaped night lamp (off), pink digital alarm clock, "
        "glass water cup, white wireless phone charger, "
        "RIGHT: white double-door wardrobe, "
        "LEFT BY WINDOW: white vanity table with round mirror, basic skincare products, "
        "hairbrush, pink hair tie, small jewelry box, "
        "pink fabric laundry basket near wardrobe, "
        "south-facing window with soft daylight streaming in, curtains open, "
        "no people, empty room, high quality, detailed"
    ),
    "bedroom_night": (
        "anime style interior illustration, cozy bedroom 14sqm, nighttime, "
        "pink-purple color scheme walls, "
        "glow-in-dark star stickers glowing on wall, "
        "CENTER: 1.5m double bed with white wooden frame, light purple bedsheets, white duvet, 2 pillows, "
        "5-6 plush toys on bed against wall (rabbit, cat, hamster, small dinosaur, shiba inu), "
        "LEFT: white bedside table with moon-shaped warm night lamp glowing softly, pink digital alarm clock, "
        "glass water cup, white wireless phone charger, "
        "RIGHT: white double-door wardrobe, "
        "LEFT BY WINDOW: white vanity table with round mirror, "
        "south-facing window showing dark night sky, curtains mostly closed, "
        "warm dim lighting from moon lamp and ambient glow, cozy sleepy atmosphere, "
        "no people, empty room, high quality, detailed"
    ),
    "kitchen_day": (
        "anime style interior illustration, small kitchen 3.5sqm, daytime, "
        "white tile walls, clean and tidy, open half-partition connecting to living room, "
        "single-door small fridge with cute magnets (cat, landmark, hotpot), "
        "double-burner gas stove with range hood above, "
        "stainless steel sink with dish soap beside, "
        "white microwave on counter left side, "
        "small pink rice cooker on counter right side, "
        "white electric kettle, "
        "wall-mounted dish rack above sink with bowls and plates, "
        "wooden knife rack with pink knife set (cleaver, fruit knife, scissors), "
        "wall-mounted spice rack (soy sauce, vinegar, salt, sugar, cooking wine, chili sauce), "
        "white upper cabinets and lower cabinets, "
        "pink apron hanging on hook by door printed COOKING IS LOVE, "
        "bright daylight, warm lighting, no people, empty room, high quality, detailed"
    ),
    "kitchen_night": (
        "anime style interior illustration, small kitchen 3.5sqm, nighttime, "
        "white tile walls, clean and tidy, open half-partition connecting to living room, "
        "single-door small fridge with cute magnets (cat, landmark, hotpot), "
        "double-burner gas stove with range hood above, "
        "stainless steel sink with dish soap beside, "
        "white microwave on counter left side, "
        "small pink rice cooker on counter right side, "
        "white electric kettle, "
        "wall-mounted dish rack above sink, "
        "wooden knife rack with pink knife set, "
        "wall-mounted spice rack, "
        "white upper cabinets and lower cabinets, "
        "pink apron hanging on hook, "
        "warm ceiling light on, night atmosphere, window showing dark outside, "
        "no people, empty room, high quality, detailed"
    ),
    "bathroom_day": (
        "anime style interior illustration, clean bathroom 3.5sqm, daytime, "
        "white ceramic sink with mirror cabinet above, "
        "white toilet on left side with toilet paper holder, "
        "glass-partition shower area in back with shower head, "
        "pink bath towel and face towel on towel rack, "
        "small white front-loading washing machine on right side, "
        "laundry detergent and softener on shelf above washer, "
        "bathroom anti-slip slippers on floor, "
        "bright white lighting, white tiles, "
        "no people, empty room, high quality, detailed"
    ),
    "bathroom_night": (
        "anime style interior illustration, clean bathroom 3.5sqm, nighttime, "
        "white ceramic sink with mirror cabinet above, "
        "white toilet on left side, "
        "glass-partition shower area in back with shower head, "
        "pink bath towel and face towel on towel rack, "
        "small white front-loading washing machine on right side, "
        "warm soft ceiling light, slightly dim cozy atmosphere, white tiles, "
        "no people, empty room, high quality, detailed"
    ),
    "balcony_day": (
        "anime style illustration, balcony 4sqm, south-facing, 12th floor view, daytime, "
        "iron railing, sliding glass door connecting to living room, "
        "white folding small table in center, "
        "two rattan wicker chairs beside table, "
        "3-tier iron plant shelf on left with potted plants (pothos, spider plant, mint, small tomato plant with fruits), "
        "clothes drying rod on ceiling with some hanging clothes, "
        "small fuzzy blanket draped on one chair, "
        "small binoculars on windowsill, "
        "city skyline in distance with mountains, "
        "bright blue sky with white clouds, warm afternoon sunlight, "
        "no people, empty, high quality, detailed"
    ),
    "balcony_night": (
        "anime style illustration, balcony 4sqm, south-facing, 12th floor view, nighttime, "
        "iron railing, sliding glass door connecting to living room with warm light inside, "
        "white folding small table in center, "
        "two rattan wicker chairs beside table, "
        "3-tier iron plant shelf on left with potted plants, "
        "small fuzzy blanket draped on one chair, "
        "small binoculars on windowsill, "
        "city skyline with glowing lights in distance, dark mountains silhouette, "
        "dark blue night sky with stars visible, moonlight, "
        "no people, empty, high quality, detailed"
    ),
}

# ============================================================
# Scene templates - loaded from scenes/ config files
# ============================================================
from scenes import SCENE_LIVING_ROOM, SCENE_BEDROOM, SCENE_KITCHEN, SCENE_BATHROOM, SCENE_BALCONY, ALL_SCENES


# ============================================================
# Generation functions
# ============================================================

def gen_backgrounds():
    print("\n========== BACKGROUNDS ==========")
    for scene, prompt in BACKGROUNDS.items():
        out_path = f"{OUT}/backgrounds/bg_{scene}.png"
        if os.path.exists(out_path):
            print(f"  Skip: {out_path}")
            continue
        print(f"\n  Generating: bg_{scene}")
        pid, imgs = text_to_image(prompt, width=BG_W, height=BG_H, prefix=f"bg_{scene}")
        download_image(imgs[0]["filename"], imgs[0]["subfolder"], out_path)


def gen_sprites(outfits, label):
    print(f"\n========== SPRITES ({label}) ==========")
    exprs = ["smile", "neutral", "shy", "sleepy"]
    for oid, outfit in outfits.items():
        for expr in exprs:
            fname = f"standing_{expr}_{oid}.png"
            raw_path = f"{OUT}/sprites/character/raw/{fname}"
            cut_path = f"{OUT}/sprites/character/{fname}"
            if os.path.exists(cut_path):
                print(f"  Skip: {cut_path}")
                continue
            prompt = (
                f"{STYLE}, {CHAR_ID}, "
                f"{EXPR[expr]}, wearing {outfit}, "
                "standing pose, full body, facing viewer, feet visible, "
                "solid bright green background, green screen, chroma key"
            )
            print(f"\n  Generating: {fname}")
            pid, imgs = text_to_image(prompt, width=SPRITE_W, height=SPRITE_H, prefix=f"sprite_{oid}")
            os.makedirs(os.path.dirname(raw_path), exist_ok=True)
            download_image(imgs[0]["filename"], imgs[0]["subfolder"], raw_path)
            cutout_green(raw_path, cut_path)


def gen_scene_images(scene_name, scene_list):
    print(f"\n========== SCENE: {scene_name} ==========")

    # Check that both day and night backgrounds exist
    bg_day_key = f"{scene_name}_day"
    bg_night_key = f"{scene_name}_night"
    bg_day_path = f"{OUT}/backgrounds/bg_{bg_day_key}.png"
    bg_night_path = f"{OUT}/backgrounds/bg_{bg_night_key}.png"
    if not os.path.exists(bg_day_path) and not os.path.exists(bg_night_path):
        print(f"  ERROR: no bg found for {scene_name}, run bg first")
        return

    for action, expr, idle_desc, engaged_desc, time_tag in scene_list:
        # Determine which time variants to generate
        if time_tag == "both":
            time_variants = ["day", "night"]
        elif time_tag == "day":
            time_variants = ["day"]
        else:
            time_variants = ["night"]

        for time_val in time_variants:
            bg_path = bg_day_path if time_val == "day" else bg_night_path
            if not os.path.exists(bg_path):
                print(f"  WARN: bg not found: {bg_path}, skipping")
                continue

            # --- Outfit selection ---
            if scene_name == "bedroom":
                if time_val == "night":
                    default_outfit = HOME_OUTFITS["H05"]  # pajama
                    ref_sprite = f"{OUT}/sprites/character/standing_smile_H05.png"
                else:
                    default_outfit = HOME_OUTFITS["H07"]  # crop top + skirt
                    ref_sprite = f"{OUT}/sprites/character/standing_smile_H07.png"
            elif scene_name == "kitchen":
                default_outfit = HOME_OUTFITS["H07"] + ", wearing pink COOKING IS LOVE apron over clothes"
                ref_sprite = f"{OUT}/sprites/character/standing_smile_H07.png"
            elif scene_name == "bathroom" and action == "towel":
                default_outfit = HOME_OUTFITS["H10"]  # towel
                ref_sprite = f"{OUT}/sprites/character/standing_smile_H10.png"
            elif scene_name == "bathroom":
                default_outfit = HOME_OUTFITS["H01"]  # pink hoodie for non-towel bathroom
                ref_sprite = f"{OUT}/sprites/character/standing_smile_H01.png"
            else:
                default_outfit = HOME_OUTFITS["H07"]  # black crop top + skirt
                ref_sprite = f"{OUT}/sprites/character/standing_smile_H07.png"

            for mode, desc in [("idle", idle_desc), ("engaged", engaged_desc)]:
                fname = f"{scene_name}_{action}_{expr}_{mode}_{time_val}.png"
                out_path = f"{OUT}/scenes/{fname}"
                if os.path.exists(out_path):
                    print(f"  Skip: {out_path}")
                    continue

                # Build edit prompt in Chinese (Qwen understands Chinese better)
                edit_prompt = (
                    f"在这个房间中画一个动漫少女，"
                    f"粉色到紫色渐变双马尾长发过腰，紫蓝色大眼睛，白皙皮肤微微脸红，"
                    f"穿着{default_outfit}，"
                    f"{desc}，"
                    f"anime style, masterpiece, best quality, consistent lighting with background"
                )

                print(f"\n  Generating: {fname}")
                try:
                    if os.path.exists(ref_sprite):
                        pid, imgs = image_edit_2(bg_path, ref_sprite, edit_prompt, prefix=f"scene_{scene_name}")
                    else:
                        pid, imgs = image_edit_1(bg_path, edit_prompt, prefix=f"scene_{scene_name}")
                    download_image(imgs[0]["filename"], imgs[0]["subfolder"], out_path)
                except Exception as e:
                    print(f"  ERROR: {e}")


def main():
    cat = sys.argv[1] if len(sys.argv) > 1 else "all"

    if cat in ("bg", "all"):
        gen_backgrounds()
    if cat in ("sprite_home", "all"):
        gen_sprites(HOME_OUTFITS, "home")
    if cat in ("sprite_out", "all"):
        gen_sprites(OUT_OUTFITS, "out")
    if cat in ("scene_lr", "all"):
        gen_scene_images("living_room", SCENE_LIVING_ROOM)
    if cat in ("scene_br", "all"):
        gen_scene_images("bedroom", SCENE_BEDROOM)
    if cat in ("scene_kt", "all"):
        gen_scene_images("kitchen", SCENE_KITCHEN)
    if cat in ("scene_bt", "all"):
        gen_scene_images("bathroom", SCENE_BATHROOM)
    if cat in ("scene_bl", "all"):
        gen_scene_images("balcony", SCENE_BALCONY)

    print("\n========== DONE ==========")


if __name__ == "__main__":
    main()
