import requests, json

base = 'http://127.0.0.1:8000'
r = requests.get(f'{base}/history')
hist = r.json()

for idx, pid in enumerate(hist.keys()):
    item = hist[pid]
    prompt = item.get('prompt', [])
    api_prompt = prompt[2]
    outputs = item.get('outputs', {})
    
    print(f'\n=== History #{idx}: {pid[:16]} ===')
    for nid, node in api_prompt.items():
        ct = node.get('class_type', '?')
        inputs = node.get('inputs', {})
        text_vals = {k: v[:80] for k, v in inputs.items() if isinstance(v, str) and len(v) > 3}
        if text_vals:
            print(f'  [{nid}] {ct} -> {text_vals}')
        else:
            print(f'  [{nid}] {ct}')
    
    print(f'  Outputs: {list(outputs.keys())}')
    for oid, odata in outputs.items():
        if 'images' in odata:
            for img in odata['images']:
                print(f'    Image: {img}')
