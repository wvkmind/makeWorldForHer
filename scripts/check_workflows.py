import json, os

wf_dir = r"C:\comfyUi\user\default\workflows"

for fname in os.listdir(wf_dir):
    if not fname.endswith('.json'):
        continue
    path = os.path.join(wf_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    print(f"\n=== {fname} ({len(nodes)} nodes) ===")
    
    for node in nodes:
        ntype = node.get('type', '?')
        title = node.get('title', '')
        nid = node.get('id', '?')
        widgets = node.get('widgets_values', [])
        
        # Show interesting nodes
        if any(k in ntype.lower() for k in ['load', 'save', 'primitive', 'prompt', 'text']):
            w_str = str(widgets)[:120] if widgets else ''
            print(f"  [{nid}] {ntype} {title} -> {w_str}")
        elif 'image' in ntype.lower() or 'Image' in ntype:
            print(f"  [{nid}] {ntype} {title}")
