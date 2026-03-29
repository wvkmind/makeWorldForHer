import requests, json

base = 'http://127.0.0.1:8000'
r = requests.get(f'{base}/history')
hist = r.json()
first_id = list(hist.keys())[0]
prompt = hist[first_id]['prompt'][2]

print("=== LoadImage nodes ===")
for nid, node in prompt.items():
    if node.get('class_type') == 'LoadImage':
        inputs = node['inputs']
        print(f"  [{nid}] image={inputs.get('image')}")

print("\n=== TextEncode nodes (prompts) ===")
for nid, node in prompt.items():
    ct = node.get('class_type', '')
    if 'TextEncode' in ct or 'PrimitiveString' in ct:
        inputs = node['inputs']
        for k, v in inputs.items():
            if isinstance(v, str) and len(v) > 0:
                print(f"  [{nid}] {ct}: {k}={v[:100]}")

print("\n=== FluxKontextImageScale nodes ===")
for nid, node in prompt.items():
    if 'FluxKontext' in node.get('class_type', ''):
        inputs = node['inputs']
        print(f"  [{nid}] {node['class_type']}: inputs={inputs}")

print("\n=== Full node list ===")
for nid, node in sorted(prompt.items()):
    ct = node.get('class_type', '?')
    print(f"  [{nid}] {ct}")
