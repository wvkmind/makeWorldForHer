"""Pipeline: scene image -> video -> frame sequence for animation."""
import os
import subprocess
from comfyui_api import image_to_video, download_image

SCENE_IMG = "xiaoai_app/assets/scenes/living_room_sitting_smile.png"
VIDEO_OUT = "xiaoai_app/assets/video/living_room_sitting_smile.mp4"
FRAMES_DIR = "xiaoai_app/assets/frames/living_room_sitting_smile"

# --- Step 1: Generate video from scene image ---
print("=== Step 1: Image to Video ===")
prompt = "微微点头微笑，头发轻轻飘动，眨眼"
pid, outputs = image_to_video(SCENE_IMG, prompt, prefix="video/xiaoai_scene")

# Download video
os.makedirs(os.path.dirname(VIDEO_OUT), exist_ok=True)
for out in outputs:
    fname = out["filename"]
    subfolder = out.get("subfolder", "")
    download_image(fname, subfolder, VIDEO_OUT)
    break

# --- Step 2: Extract frames ---
print("\n=== Step 2: Extract frames ===")
os.makedirs(FRAMES_DIR, exist_ok=True)
cmd = [
    "ffmpeg", "-y", "-i", VIDEO_OUT,
    "-vf", "fps=12",  # 12 fps for smooth loop
    os.path.join(FRAMES_DIR, "frame_%04d.png")
]
subprocess.run(cmd, check=True)

frame_count = len([f for f in os.listdir(FRAMES_DIR) if f.endswith(".png")])
print(f"\nDone! Extracted {frame_count} frames to {FRAMES_DIR}")
