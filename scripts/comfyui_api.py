"""ComfyUI API helper - text2img, img2img (1/2/3 ref), img2video, cutout."""
import requests
import json
import time
import os
import random
import copy
import numpy as np
from PIL import Image

COMFYUI_URL = "http://127.0.0.1:8000"
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "workflows", "api_format")


def queue_prompt(prompt):
    r = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": prompt})
    r.raise_for_status()
    return r.json()


def get_history(prompt_id):
    r = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
    return r.json()


def wait_for_result(prompt_id, timeout=600, poll=2):
    start = time.time()
    while time.time() - start < timeout:
        hist = get_history(prompt_id)
        if prompt_id in hist:
            status = hist[prompt_id].get("status", {})
            if status.get("completed"):
                return hist[prompt_id]
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI error: {status}")
        time.sleep(poll)
    raise TimeoutError(f"Prompt {prompt_id} timed out after {timeout}s")


def download_image(filename, subfolder, output_path):
    r = requests.get(f"{COMFYUI_URL}/view",
                     params={"filename": filename, "subfolder": subfolder, "type": "output"})
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(r.content)
    print(f"  Downloaded: {output_path}")
    return output_path


def upload_image(filepath):
    fname = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        r = requests.post(f"{COMFYUI_URL}/upload/image",
                          files={"image": (fname, f, "image/png")})
    result = r.json()
    print(f"  Uploaded: {result.get('name', fname)}")
    return result.get("name", fname)


def _get_output_images(hist):
    images = []
    for nid, odata in hist.get("outputs", {}).items():
        if "images" in odata:
            for img in odata["images"]:
                images.append(img)
    return images


def _load_template(name):
    path = os.path.join(TEMPLATE_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Text to Image (Flux2 Klein 9B)
# ============================================================
def text_to_image(prompt_text, width=768, height=1024, seed=None, prefix="xiaoai"):
    if seed is None:
        seed = random.randint(0, 2**53)

    api = {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "flux-2-klein-base-9b-fp8.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen_3_8b_fp8mixed.safetensors", "type": "flux2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "flux2-vae.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt_text}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": ""}},
        "6": {"class_type": "EmptyFlux2LatentImage", "inputs": {
            "width": width, "height": height, "batch_size": 1}},
        "7": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "8": {"class_type": "Flux2Scheduler", "inputs": {
            "steps": 20, "width": width, "height": height}},
        "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "10": {"class_type": "CFGGuider", "inputs": {
            "model": ["1", 0], "positive": ["4", 0], "negative": ["5", 0], "cfg": 5.0}},
        "11": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["7", 0], "guider": ["10", 0], "sampler": ["9", 0],
            "sigmas": ["8", 0], "latent_image": ["6", 0]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "13": {"class_type": "SaveImage", "inputs": {
            "filename_prefix": prefix, "images": ["12", 0]}},
    }

    result = queue_prompt(api)
    pid = result["prompt_id"]
    print(f"[text2img] Queued: {pid}")
    hist = wait_for_result(pid)
    return pid, _get_output_images(hist)


# ============================================================
# Image Edit - 1 image (Qwen Image Edit)
# ============================================================
def image_edit_1(image_path, prompt_text, seed=None, prefix="edit1"):
    if seed is None:
        seed = random.randint(0, 2**53)
    
    uploaded = upload_image(image_path)
    api = _load_template("history_6_1img_success.json")
    
    # Set inputs
    api["78"]["inputs"]["image"] = uploaded
    api["435"]["inputs"]["value"] = prompt_text
    api["433:3"]["inputs"]["seed"] = seed
    api["60"]["inputs"]["filename_prefix"] = prefix
    
    result = queue_prompt(api)
    pid = result["prompt_id"]
    print(f"[edit1] Queued: {pid}")
    hist = wait_for_result(pid)
    return pid, _get_output_images(hist)


# ============================================================
# Image Edit - 2 images (Qwen Image Edit)
# ============================================================
def image_edit_2(image1_path, image2_path, prompt_text, seed=None, prefix="edit2"):
    if seed is None:
        seed = random.randint(0, 2**53)
    
    uploaded1 = upload_image(image1_path)
    uploaded2 = upload_image(image2_path)
    api = _load_template("history_8_2img_error.json")
    
    api["78"]["inputs"]["image"] = uploaded1
    api["437"]["inputs"]["image"] = uploaded2
    api["435"]["inputs"]["value"] = prompt_text
    api["433:3"]["inputs"]["seed"] = seed
    api["60"]["inputs"]["filename_prefix"] = prefix
    
    result = queue_prompt(api)
    pid = result["prompt_id"]
    print(f"[edit2] Queued: {pid}")
    hist = wait_for_result(pid)
    return pid, _get_output_images(hist)


# ============================================================
# Image Edit - 3 images (Qwen Image Edit)
# ============================================================
def image_edit_3(image1_path, image2_path, image3_path, prompt_text, seed=None, prefix="edit3"):
    if seed is None:
        seed = random.randint(0, 2**53)
    
    uploaded1 = upload_image(image1_path)
    uploaded2 = upload_image(image2_path)
    uploaded3 = upload_image(image3_path)
    api = _load_template("history_7_3img_error.json")
    
    api["78"]["inputs"]["image"] = uploaded1
    api["437"]["inputs"]["image"] = uploaded2
    api["438"]["inputs"]["image"] = uploaded3
    api["435"]["inputs"]["value"] = prompt_text
    api["433:3"]["inputs"]["seed"] = seed
    api["60"]["inputs"]["filename_prefix"] = prefix
    
    result = queue_prompt(api)
    pid = result["prompt_id"]
    print(f"[edit3] Queued: {pid}")
    hist = wait_for_result(pid)
    return pid, _get_output_images(hist)


# ============================================================
# Image to Video (Wan2.2 14B i2v)
# ============================================================
def image_to_video(image_path, prompt_text, negative_prompt=None, seed=None, prefix="video/xiaoai"):
    if seed is None:
        seed = random.randint(0, 2**53)
    if negative_prompt is None:
        negative_prompt = "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部"
    
    uploaded = upload_image(image_path)
    api = _load_template("history_1_1img_success.json")
    
    api["97"]["inputs"]["image"] = uploaded
    api["129:93"]["inputs"]["text"] = prompt_text
    api["129:89"]["inputs"]["text"] = negative_prompt
    api["108"]["inputs"]["filename_prefix"] = prefix
    # Set seed on both KSamplerAdvanced nodes
    api["129:86"]["inputs"]["noise_seed"] = seed
    api["129:85"]["inputs"]["noise_seed"] = seed
    
    result = queue_prompt(api)
    pid = result["prompt_id"]
    print(f"[i2v] Queued: {pid}")
    hist = wait_for_result(pid, timeout=1200)
    return pid, _get_output_images(hist)


# ============================================================
# Green screen cutout
# ============================================================
def cutout_green(input_path, output_path=None):
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_cutout.png"
    
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img, dtype=np.float32)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    
    # Green screen detection
    green_mask = (g > 100) & (g > r * 1.3) & (g > b * 1.3)
    green_strength = np.clip((g - np.maximum(r, b)) / 80.0, 0, 1)
    alpha = np.where(green_mask, (1.0 - green_strength) * 255, 255).astype(np.uint8)
    
    result_data = np.array(img)
    result_data[:,:,3] = alpha
    
    # Despill: remove green tint from edges
    edge_mask = (alpha > 0) & (alpha < 250)
    if np.any(edge_mask):
        max_rb = np.maximum(result_data[:,:,0], result_data[:,:,2])
        result_data[:,:,1] = np.where(edge_mask, np.minimum(result_data[:,:,1], max_rb), result_data[:,:,1])
    
    try:
        from scipy.ndimage import binary_dilation
        edge_dilated = binary_dilation(edge_mask, iterations=2)
        opaque_near_edge = edge_dilated & (alpha == 255)
        if np.any(opaque_near_edge):
            max_rb2 = np.maximum(result_data[:,:,0], result_data[:,:,2])
            excess = np.clip(result_data[:,:,1].astype(np.int16) - max_rb2.astype(np.int16), 0, 255).astype(np.uint8)
            result_data[:,:,1] = np.where(opaque_near_edge,
                result_data[:,:,1] - (excess * 0.7).astype(np.uint8), result_data[:,:,1])
    except ImportError:
        pass
    
    result = Image.fromarray(result_data)
    bbox = result.getbbox()
    if bbox:
        result = result.crop(bbox)
    
    result.save(output_path)
    print(f"  Cutout: {result.size} -> {output_path}")
    return output_path
