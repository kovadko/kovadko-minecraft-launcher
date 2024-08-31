import random
import uuid

from flask import Flask, jsonify, render_template
from flask import request

from utils import (
    Config,
    get_installed_versions,
    get_vanilla_versions, 
    get_versions_supported_by_forge, 
    get_versions_supported_by_fabric, 
    get_versions_supported_by_quilt,
    launch_minecraft,
    install_minecraft
)

launcher_settings = Config('launcher_settings.json')

command_args = Config('command_args.json')

if command_args.data["username"] == "":
    command_args.update({"username": f"player-{random.randrange(100, 1000)}",})

command_args.update({"uuid": str(uuid.uuid4())})

version, modification = launcher_settings.data['minecraft_to_launch'].values()

app = Flask(__name__)

@app.route('/update_minecraft_to_launch', methods=['POST'])
def update_minecraf_to_launch():
    global version, modification
    version, modification = request.get_json().values()
    
    return jsonify({'message': 'minecraft_to_launch successfully updated.'})

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'play' in request.form:
            launch_minecraft(version, modification, command_args.data)
        
        if 'install' in request.form:
            install_minecraft(version, modification)

            launcher_settings.update({'minecraft_to_launch': {'version': version, 'modification': modification}})

            if launcher_settings.data['run_after_install']:
                launch_minecraft(version, modification, command_args.data)
                  
    return render_template('main.html', version_to_launch=f'{version} {modification}' if modification else version)

@app.route('/versions/installed')
def get_installed():
    return jsonify(get_installed_versions())

@app.route('/versions/vanilla')
def get_vanila():
    versions = get_vanilla_versions()

    vanilla_versions = []
    for key in launcher_settings.data['show_in_vanilla_versions']:
        vanilla_versions += versions.get(key)

    return jsonify(vanilla_versions)

@app.route('/versions/forge')
def get_forge():
    return jsonify(get_versions_supported_by_forge())

@app.route('/versions/fabric')
def get_fabric():
    return jsonify(get_versions_supported_by_fabric())

@app.route('/versions/quilt')
def get_quilt():
    return jsonify(get_versions_supported_by_quilt())

if __name__ == '__main__':
    app.run(debug=True)