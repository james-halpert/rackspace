# Network Rack Tracker

A lightweight Flask-based tool for visually planning and tracking network rack layouts, device port assignments, and interconnections — all with zero database dependencies.

## ✨ Features

- 📦 Add multiple racks with defined unit capacity
- 🔌 Add devices with custom port counts and assign them to specific U positions
- 🔗 Map connections between device ports (validated against used ports)
- 🧠 Freeform notes section for project context and build references
- 📄 Import/export full layout as JSON (includes racks, devices, connections, notes)
- 🖥 Visual rack view with clickable ports and connection highlights
- 🔥 Collision prevention (prevents multiple devices from using the same rack + U)
- 😎 Fully local, no internet required

## 🛠 Getting Started

1. Clone this repo:
   ```bash
   git clone https://github.com/james-halpert/rackspace.git
   cd rackspace
   ```

2. Install dependencies (Python 3.7+ recommended):
   ```bash
   pip install flask
   ```

3. Run the app:
   ```bash
   python network_rack_tracker.py
   ```

4. Visit [http://localhost:5000](http://localhost:5000) in your browser.
5. Visit [http://localhost:5000/rackview](http://localhost:5000/rackview) in your browser for a fancy view of the rack.

## 🗃 Project Layout

```bash
.
├── network_rack_tracker.py  # Flask app
├── templates/
│   ├── index.html           # Main form interface
│   └── rackview.html        # Rack visualization
└── static/                  # (Optional) for CSS/JS assets if needed
```

## 🔐 Notes

This app stores all data in memory while running. Use the **Export** button to save your progress between sessions. Imported files restore your full working state, including devices, connections, racks, and notes.

## 📸 Screenshots

> ![image](https://github.com/user-attachments/assets/4c80244d-3244-4a84-9919-63530a32deb7)


## 🧑‍💻 Author

**Arlen Kirkaldie**  
Designed for real-world IT field work and sanity.

---

Hack the Gibson and keep the stack noted!
