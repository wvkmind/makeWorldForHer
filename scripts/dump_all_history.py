import requests, json, os

base = 'http://127.0.0.1:8000'
r = requests.get(f'{base}/history')
hist = r.json()

out_dir = 'docs/workflows/api_format'
os.makedirs(out_dir, exist_ok=True)

print(f"Total history items: {len(hist)}")

for idx, pid in enumerate(hist.keys()):
    item = hist[pid]
    prompt = item.get('prompt', [])
    if len(prompt) < 3:
        print(f"  #{idx} {pid[:16]}: no prompt data")
        continue
    
    api_prompt = prompt[2]
    status = item.get('status', {}).get('status_str', '?')
    
    # Count LoadImage nodes
    load_images = []
    prompt_texts = []
    for nid, node in api_prompt.items():
        ct = node.get('class_type', '')
        if ct == 'LoadImage':
            load_images.append(node['inputs'].get('image', '?'))
        if 'PrimitiveString' in ct:
            val = node['inputs'].get('value', '')
            if val:
                prompt_texts.append(val[:60])
    
    label = f"history_{idx}_{len(load_images)}img_{status}"
    print(f"  #{idx} [{pid[:16]}] status={status} images={load_images} prompt={prompt_texts}")
    
    # Save API format
    out_path = os.path.join(out_dir, f"{label}.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(api_prompt, f, indent=2, ensure_ascii=False)
    print(f"    -> saved to {out_path}")
