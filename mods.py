# What goes into each server mod folder. Used by clipons/install.py (the author's own test install) and
# make_release.py (the public package), and REPO by converter/make_scripts.py. The public mod holds the AN/PVS-27,
# AN/PVS-30 and UTC XII: the AN/PVS-30 ships its bundle (3DMA's licence allows free Tarkov mods); the AN/PVS-27
# and UTC XII ship model-free templates and a build script each, which players run on their own CGTrader purchase
# (those terms are read strictly). The AN/PVS-22 is the author's private build only (its TurboSquid model is
# licensed for editorial use only, which rules out games). Both mods share one client plugin.
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = 'UstAchae/K-ClipOnSight'
PVS22, CLIPONS = W / 'pvs22', W / 'clipons'

BASE_DEPS = ['shaders', 'cubemaps', 'assets/systems/effects/opticsight/opticsightsmasks.bundle']
THERMAL_DEPS = BASE_DEPS + ['assets/content/items/mods/scopes/scope_base_trijicon_reap-ir.bundle',
                            'assets/systems/effects/nightvision.bundle', 'assets/systems/effects/nightvision/mask_nv_textures']

PLUGIN_FOLDER = 'UstAchae-ClipOnSight'
PLUGIN_DLL = PVS22 / 'package/client/UstAchae.ClipOnSight.Client.dll'
TOP_RAILS = PVS22 / 'package/db/top_rails.json'
BUNDLES = CLIPONS / 'package/bundles/ustachae_clipons'
ITEMS = CLIPONS / 'package/db/items'

# key: the mod's folder, its server assembly (built by pvs22/ServerSource/build.sh into bin/Release/<key>/),
# its items (catalog file -> name under db/items/), its bundles (bundle key -> built file, dependencies), whether
# it is published, the bundles its release ships, and its players' build scripts (script -> the bundles it writes).
MODS = {
    'all': {'folder': 'UstAchae-ClipOnSight', 'assembly': 'UstAchae.ClipOnSight', 'public': True,
            'items': {ITEMS / f'{n}.json': f'{n}.json' for n in ('pvs27', 'pvs27_fde', 'pvs30', 'utc', 'utc_fde')},
            'bundles': {'ustachae_clipons/pvs27.bundle': (BUNDLES / 'pvs27.bundle', BASE_DEPS),
                        'ustachae_clipons/pvs27_fde.bundle': (BUNDLES / 'pvs27_fde.bundle', BASE_DEPS),
                        'ustachae_clipons/pvs30.bundle': (BUNDLES / 'pvs30.bundle', BASE_DEPS),
                        'ustachae_clipons/utc.bundle': (BUNDLES / 'utc.bundle', THERMAL_DEPS),
                        'ustachae_clipons/utc_fde.bundle': (BUNDLES / 'utc_fde.bundle', THERMAL_DEPS)},
            'shipped': ['ustachae_clipons/pvs30.bundle'],
            'scripts': {'build_pvs27.py': ['ustachae_clipons/pvs27.bundle', 'ustachae_clipons/pvs27_fde.bundle'],
                        'build_utc.py': ['ustachae_clipons/utc.bundle', 'ustachae_clipons/utc_fde.bundle']}},
    'pvs22': {'folder': 'UstAchae-ClipOnSight-PVS22', 'assembly': 'UstAchae.ClipOnSight.PVS22', 'public': False,
              'items': {PVS22 / 'package/db/pvs22.json': 'pvs22.json'},
              'bundles': {'ustachae_pvs22/an_pvs22.bundle': (PVS22 / 'package/bundles/ustachae_pvs22/an_pvs22.bundle', BASE_DEPS)},
              'shipped': ['ustachae_pvs22/an_pvs22.bundle'], 'scripts': {}},
}


def server_files(key):
    """The server mod's assembly files: name in the mod folder -> built file."""
    out, name = PVS22 / 'ServerSource/bin/Release' / key, MODS[key]['assembly']
    return {f'{name}{ext}': out / f'{name}{ext}' for ext in ('.dll', '.deps.json', '.runtimeconfig.json')}


def manifest(key, bundles=None):
    """bundles.json for a mod: the given bundle keys, or all of them."""
    mod = MODS[key]
    return {'manifest': [{'key': b, 'dependencyKeys': mod['bundles'][b][1]} for b in (bundles or mod['bundles'])]}
