#!/usr/bin/env python3
"""Verify and create a deterministic ZIP with an internal SHA-256 manifest."""
import argparse
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','__pycache__','.venv','node_modules','.DS_Store'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    if output.is_relative_to(ROOT): raise SystemExit('Choose an output outside the repository to avoid recursive archives.')
    subprocess.run([sys.executable,str(ROOT/'scripts/verify.py')],check=True)
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink()
                 and not any(part in EXCLUDED for part in p.relative_to(ROOT).parts)
                 and p.suffix not in {'.zip','.pyc'} and p.name!='SHA256SUMS.txt')
    manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,content in [(p.relative_to(ROOT).as_posix(),p.read_bytes()) for p in files]+[('SHA256SUMS.txt',manifest.encode())]:
            info=zipfile.ZipInfo('Extra-Universal-Kennedy/'+name,date_time=(2026,10,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.create_system=3; info.external_attr=0o100644<<16
            z.writestr(info,content)
    with zipfile.ZipFile(output) as z:
        bad=z.testzip()
        if bad: raise SystemExit('ZIP CRC failure: '+bad)
    print(f'Created {output.name}: {len(files)+1} entries; {output.stat().st_size:,} bytes.')
    print('ZIP SHA-256: '+hashlib.sha256(output.read_bytes()).hexdigest())

if __name__=='__main__': main()
