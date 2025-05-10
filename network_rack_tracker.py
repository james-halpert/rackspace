from flask import Flask, render_template, request, redirect, url_for, session, send_file
from io import BytesIO
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

devices = []
connections = []
racks = []
notes = ""

@app.route('/')
def index():
    src_idx = session.get('src_idx', 0)
    dst_idx = session.get('dst_idx', 1 if len(devices) > 1 else 0)

    if src_idx >= len(devices):
        src_idx = 0
        session['src_idx'] = 0
    if dst_idx >= len(devices):
        dst_idx = 0
        session['dst_idx'] = 0

    used_ports = {}
    available_ports = {}

    for d in devices:
        key = d['name'].lower().replace(' ', '_')
        used_ports[key] = []
        start = d.get('port_start', 0)
        available_ports[key] = list(range(start, start + d['ports']))

    for c in connections:
        try:
            src_name, src_port = c['src'].split(' Port ')
            dst_name, dst_port = c['dest'].split(' Port ')
            if src_port.strip().isdigit():
                used_ports[src_name.lower().replace(' ', '_')].append(int(src_port))
            if dst_port.strip().isdigit():
                used_ports[dst_name.lower().replace(' ', '_')].append(int(dst_port))
        except ValueError:
            # Log or skip bad connection entries
            continue


    for k in used_ports:
        available_ports[k] = [p for p in available_ports[k] if p not in used_ports[k]]

    return render_template('index.html', devices=devices, racks=racks, connections=connections,
                           available_ports=available_ports, src_idx=src_idx, dst_idx=dst_idx, notes=notes, error=session.pop('error', None))

@app.route('/add_device', methods=['POST'])
def add_device():
    name = request.form.get('name', '').strip()
    rack_id = request.form.get('rack_id', '').strip()

    try:
        ports = int(request.form.get('ports', 0))
        port_start = int(request.form.get('port_start', 0))
        u_position = int(request.form.get('u_position', 0))
    except (ValueError, TypeError) as e:
        session['error'] = f"Invalid numeric input: {e}"
        return redirect(url_for('index'))

    devices.append({
        'name': name,
        'ports': ports,
        'port_start': port_start,
        'rack_id': rack_id,
        'u_position': u_position
    })

    return redirect(url_for('index'))


@app.route('/add_rack', methods=['POST'])
def add_rack():
    rack_id = request.form['rack_id']
    units = int(request.form['units'])

    for r in racks:
        if r['id'] == rack_id:
            session['error'] = f"Rack '{rack_id}' already exists."
            return redirect(url_for('index'))

    racks.append({
        'id': rack_id,
        'units': units
    })
    return redirect(url_for('index'))

@app.route('/set_selection', methods=['POST'])
def set_selection():
    session['src_idx'] = int(request.form['src_device'])
    session['dst_idx'] = int(request.form['dest_device'])
    return redirect(url_for('index'))

@app.route('/add_connection', methods=['POST'])
def add_connection():
    src_index = int(request.form['src_device'])
    dst_index = int(request.form['dest_device'])
    src_port = request.form['src_port']
    dst_port = request.form['dest_port']
    connections.append({
        'src': f"{devices[src_index]['name']} Port {src_port}",
        'dest': f"{devices[dst_index]['name']} Port {dst_port}"
    })
    return redirect(url_for('index'))

@app.route('/delete_device/<int:index>', methods=['POST'])
def delete_device(index):
    if 0 <= index < len(devices):
        del devices[index]
    return redirect(url_for('index'))

@app.route('/delete_connection/<int:index>', methods=['POST'])
def delete_connection(index):
    if 0 <= index < len(connections):
        del connections[index]
    return redirect(url_for('index'))

@app.route('/update_notes', methods=['POST'])
def update_notes():
    global notes
    notes = request.form['notes']
    return redirect(url_for('index'))

@app.route('/export')
def export():
    data = {
        'devices': devices,
        'connections': connections,
        'racks': racks,
        'notes': notes
    }
    buffer = BytesIO()
    buffer.write(json.dumps(data, indent=2).encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, mimetype='application/json', as_attachment=True, download_name='rack_export.json')

@app.route('/import', methods=['POST'])
def import_json():
    global devices, connections, racks, notes
    file = request.files['file']
    if file:
        data = json.load(file)
        devices = data.get('devices', [])
        connections = data.get('connections', [])
        racks = data.get('racks', [])
        notes = data.get('notes', '')
    return redirect(url_for('index'))

@app.route('/rackview')
def rackview():
    return render_template('rackview.html', devices=devices, racks=racks, connections=connections, notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5213, debug=True)
