from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        configure_network(ssid, password)
        return redirect(url_for('success'))
    return render_template('index.html')

def get_next_filename(base_path, base_name):
    index = 100 # save room for default networks
    while True:
        new_name = f"{base_name}_{index}.nmconnection"
        full_path = os.path.join(base_path, new_name)
        if not os.path.exists(full_path):
            return full_path, index
        index += 1

def configure_network(ssid, password):
    base_path = '/etc/NetworkManager/system-connections'
    base_name = 'mywifi'
    file_path, priority = get_next_filename(base_path, base_name)
    print(f"filepath: {file_path}, priority: {priority}")

    config = f"""
[connection]
id={os.path.splitext(os.path.basename(file_path))[0]}
type=wifi
autoconnect=true
autoconnect-priority={priority}
permissions=
[wifi]
ssid={ssid}
mode=infrastructure
[ipv4]
method=auto
[wifi-security]
key-mgmt=wpa-psk
psk={password}
"""
    with open('/tmp/config.nmconnection', 'w') as f:
        f.write(config)
    subprocess.run(['sudo', 'mv', '/tmp/config.nmconnection', file_path])
    subprocess.run(['sudo', 'chmod', '600', file_path])
    subprocess.run(['sudo', 'nmcli', 'con', 'reload'])
    subprocess.run(['sudo', 'nmcli', 'con', 'up', 'id', os.path.splitext(os.path.basename(file_path))[0]])

@app.route('/success')
def success():
    return "Wi-Fi credentials updated successfully!"
