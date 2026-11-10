import os
import shutil
import hashlib
import json

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    # Dynamically resolve root workspace directory (parent of research-platform)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    public_dir = os.path.join(root, 'research-platform', 'public', 'research_data')
    os.makedirs(public_dir, exist_ok=True)

    # 1. Copy DAM_ANALYSIS_READY_2026
    dam_ready_src = os.path.join(root, 'DAM_ANALYSIS_READY_2026')
    dam_ready_dst = os.path.join(public_dir, 'DAM_ANALYSIS_READY_2026')
    if os.path.exists(dam_ready_dst):
        shutil.rmtree(dam_ready_dst)
    shutil.copytree(dam_ready_src, dam_ready_dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    print("Copied DAM_ANALYSIS_READY_2026")

    # 2. Copy dam_output key directories and files (excluding massive raw json)
    dam_out_src = os.path.join(root, 'dam_output')
    dam_out_dst = os.path.join(public_dir, 'dam_output')
    if os.path.exists(dam_out_dst):
        shutil.rmtree(dam_out_dst)
    os.makedirs(dam_out_dst, exist_ok=True)
    
    # Copy master CSVs
    shutil.copytree(os.path.join(dam_out_src, 'master'), os.path.join(dam_out_dst, 'master'))
    
    # Copy top-level metadata CSVs
    for f in os.listdir(dam_out_src):
        fp = os.path.join(dam_out_src, f)
        if os.path.isfile(fp) and f.endswith('.csv'):
            shutil.copy2(fp, os.path.join(dam_out_dst, f))
    print("Copied dam_output")

    # 3. Copy Step123
    step123_src = os.path.join(root, 'research-platform', 'Step123')
    step123_dst = os.path.join(public_dir, 'Step123')
    if os.path.exists(step123_dst):
        shutil.rmtree(step123_dst)
    shutil.copytree(step123_src, step123_dst)
    print("Copied Step123")

    # 4. Generate Master Manifest
    manifest = []
    for dirpath, _, filenames in os.walk(public_dir):
        for fn in filenames:
            if fn == 'manifest.json':
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, public_dir).replace('\\', '/')
            ext = os.path.splitext(fn)[1].lower().replace('.', '')
            sz = os.path.getsize(fp)
            h = sha256_file(fp)
            manifest.append({
                "relativePath": rel,
                "fileName": fn,
                "fileType": ext,
                "sizeBytes": sz,
                "sha256": h
            })

    with open(os.path.join(public_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f"Generated manifest.json with {len(manifest)} static files!")

if __name__ == '__main__':
    main()
