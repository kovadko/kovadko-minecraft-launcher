from lxml import etree
import requests
from pathlib import Path
import json
import jsonschema
from minecraft_launcher_lib import fabric, forge, quilt, install
import subprocess
from minecraft_launcher_lib.command import get_minecraft_command

__all__ = [
    'Config',
    'get_vanilla_versions', 
    'get_versions_supported_by_forge', 
    'get_versions_supported_by_fabric', 
    'get_versions_supported_by_quilt',
    'get_installed_versions',
    'launch_minecraft',
    'install_minecraft'
    ]

class Config:
    def __init__(self, name: str):
        self.config_path = Path('configuration', name)
        self.json_schemas_path = Path('json_schemas', name)

        if self.config_path.exists():
            with open(self.config_path) as file:
                self.config = json.load(file)

        if self.json_schemas_path.exists():
            with open(self.json_schemas_path) as file:
                self.schema = json.load(file)

        try:
            jsonschema.validate(self.config, self.schema)
            self.data = self.config
        except jsonschema.exceptions.ValidationError as e:
            print(e)
            exit(1)

    def __save(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.data, file, sort_keys=False, indent=2)

    def update(self, to_update: dict):
        for key, val in to_update.items():
            self.data.update({key: val})

        self.__save()

def get_json_data(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

def get_vanilla_versions() -> dict:
    '''Returns all vanilla versions that Mojang offers to download'''

    releases, snapshots, old_beta, old_alpha = [], [], [], []
    
    data = get_json_data('https://launchermeta.mojang.com/mc/game/version_manifest_v2.json')['versions']
    for version in data:
        if version['type'] == 'release':
            releases.append(version['id'])

        if version['type'] == 'snapshot':
            snapshots.append(version['id'])

        if version['type'] == 'old_beta':
            old_beta.append(version['id'])

        if version['type'] == 'old_alpha':
            old_alpha.append(version['id'])
    
    return {'releases': releases, 'snapshots': snapshots, 'old_beta': old_beta, 'old_alpha': old_alpha}

def get_versions_supported_by_forge() -> list:
    FORGE_API_URL = 'https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml'
    response = requests.get(FORGE_API_URL)
    response.raise_for_status()

    root = etree.fromstring(response.content)

    versions = []
    for game in root.xpath('//version/text()'):
        version = game.split('-')[0]
        if version not in versions:
            versions.append(version)

    return versions

def get_versions_supported_by_fabric() -> list:
    FABRIC_API_URL = 'https://meta.fabricmc.net/v2/versions/game'

    versions = []
    for game in get_json_data(FABRIC_API_URL):
        if game['stable']:
            versions.append(game['version'])
    
    return versions

def get_versions_supported_by_quilt() -> list:
    QUILT_API_URL = 'https://meta.quiltmc.org/v3/versions/game'

    versions = []
    for game in get_json_data(QUILT_API_URL):
        if game['stable']:
            versions.append(game['version'])
    
    return versions

MINECRAFT_DIR = Config('command_args.json').data['gameDirectory']
VERSIONS_DIR = Path(MINECRAFT_DIR, 'versions')

def get_installed_versions() -> dict:
    forge, fabric, quilt = {}, {}, {}
    vanilla = []

    if VERSIONS_DIR.exists():
        for directory in VERSIONS_DIR.iterdir():
            if 'forge' in directory.name:
                forge.update({directory.name.split('-')[-1]: directory.name})
                continue    
            if 'fabric' in directory.name:
                fabric.update({directory.name.split('-')[-1]: directory.name})
                continue
            if 'quilt' in directory.name:
                quilt.update({directory.name.split('-')[-1]: directory.name})
                continue
 
            vanilla.append(directory.name)
    return {'vanilla': vanilla, 'forge': forge, 'fabric': fabric, 'quilt': quilt}

def launch_minecraft(version: str, modification: str, command_args: list) -> None:
    installed_versions = get_installed_versions()

    if modification:
        if version in installed_versions[modification]:
            minecraft = installed_versions[modification][version]

    else:
        if version in installed_versions['vanilla']:
            minecraft = version

    command = get_minecraft_command(minecraft, MINECRAFT_DIR, command_args)
    subprocess.run(command)

def install_minecraft(version: str, modification: str | None) -> None:
    if modification == 'forge':
        forge.install_forge_version(
            version, 
            MINECRAFT_DIR, 
            callback={'setStatus': lambda logs: print(logs)}
        )
    
    if modification == 'fabric':
        fabric.install_fabric(
            version, 
            MINECRAFT_DIR, 
            callback={'setStatus': lambda logs: print(logs)}
        )

    if modification == 'quilt':
        quilt.install_quilt(
            version, 
            MINECRAFT_DIR ,
            callback={'setStatus': lambda logs: print(logs)}
        )

    else:
        install.install_minecraft_version(
            version, 
            MINECRAFT_DIR, 
            {'setStatus': lambda logs: print(logs)}
        )
