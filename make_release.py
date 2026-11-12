# Author-side: packs the public mod as one zip laid out like the game folder: the server mod with its items, the
# AN/PVS-30 bundle, the AN/PVS-27 and UTC XII build scripts with their model-free templates, and the client plugin.
# The private AN/PVS-22 is never packed.
# Usage: python make_release.py  ->  dist/JustachaesClipOnSight-<version>.zip
import json, re, zipfile
from pathlib import Path
from mods import MODS, PLUGIN_DLL, PLUGIN_FOLDER, TOP_RAILS, W, server_files, manifest

CONVERTER = W / 'converter'
VERSION = re.search(r'Version \{ get; init; \} = new\("([^"]+)"\)', (W / 'pvs22/ServerSource/PVS22Mod.cs').read_text(encoding='utf-8')).group(1)


def package(key):
    mod = MODS[key]
    folder = f'SPT_Runtime/user/mods/{mod["folder"]}/'
    files = {f'BepInEx/plugins/{PLUGIN_FOLDER}/{PLUGIN_DLL.name}': PLUGIN_DLL.read_bytes()}
    for name, src in server_files(key).items(): files[folder + name] = src.read_bytes()
    for src, name in mod['items'].items(): files[folder + 'db/items/' + name] = src.read_bytes()
    files[folder + 'db/top_rails.json'] = TOP_RAILS.read_bytes()
    for bundle in mod['shipped']: files[folder + 'bundles/' + bundle] = mod['bundles'][bundle][0].read_bytes()
    files[folder + 'bundles.json'] = json.dumps(manifest(key, mod['shipped']), indent=2).encode()
    for script, bundles in mod['scripts'].items():
        files[folder + script] = (CONVERTER / script).read_bytes()
        for bundle in bundles:
            template = CONVERTER / 'templates' / (Path(bundle).stem + '.bundle.template')
            files[folder + 'templates/' + template.name] = template.read_bytes()
    return files


def main():
    out_dir = W / 'dist'
    out_dir.mkdir(exist_ok=True)
    for key, mod in MODS.items():
        if not mod['public']: continue
        files = package(key)
        out = out_dir / f'JustachaesClipOnSight-{VERSION}.zip'
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for name, data in sorted(files.items()): z.writestr(name, data)
        print('RELEASE', out.name, f'{out.stat().st_size / 1e6:.1f} MB')
        for name in sorted(files): print('  ', name)


if __name__ == '__main__':
    main()
