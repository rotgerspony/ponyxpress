# PonyXpress Master Project Knowledge
_Last Updated: 2025-08-16 02:50:54_

---

## 🚀 Project Name
**PonyXpress** — Rural Delivery Management System with AI-powered enhancements

---

## 📦 Core Features

- 📍 Real-time GPS Tracking on Interactive Maps (Mapbox/Leaflet)
- 📨 Package Scanning with Photo Uploads & Metadata
- 🔐 Secure Login with Flask-Login + Role System
  - `carrier`, `substitute`, `admin`
- ✍️ Carriers can draw or generate traces/routes on map
- 🕵️ Substitutes can only view assigned traces
- 🧭 Offline mode with auto-sync queue
- 📂 Admin Dashboard: manage users, traces, stops, photos
- 📤 Google Drive Sync for GPX + photo data
- 📲 Fully mobile responsive + PWA ready + Android APK ready
- 🧊 Winter Mode: UI preset for snowy conditions
- 📊 Performance Panel: route completion times, scan stats

---

## 🧠 Important Command Examples (Windows PowerShell)

```powershell
# Create and activate venv
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.env\Scripts\Activate.ps1

# Install dependencies
.env\Scripts\python.exe -m pip install -r requirements.txt

# Set Flask environment & run app
$env:FLASK_APP = "app.py"
flask run
```

---

## 🗂️ Folder Structure

```
ponyxpress/
├── app.py
├── models.py
├── config.py
├── requirements.txt
├── /static/
│   ├── /uploads/
│   └── styles.css
├── /templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── map.html
│   ├── upload.html
│   ├── /admin/
│   │   └── dashboard.html
│   └── /partials/
│       └── route_preview.html
├── /views/
│   ├── __init__.py
│   ├── auth.py
│   ├── trace.py
│   ├── admin.py
├── /utils/
│   └── drive_sync.py
└── /instance/
    └── ponyxpress.db
```

---

## 🔐 Roles and Permissions

| Role       | Can View Map | Can Edit Routes | Can Scan Packages | Admin Dashboard |
|------------|--------------|-----------------|-------------------|------------------|
| `carrier`  | ✅           | ✅              | ✅                | ❌               |
| `substitute` | ✅         | ❌              | ✅ (follow only)  | ❌               |
| `admin`    | ✅           | ✅              | ✅                | ✅               |

---

## 💾 SQL Tables (via SQLAlchemy)

- `User`: id, username, password_hash, role
- `Trace`: id, user_id, date, polyline, etc.
- `Stop`: id, trace_id, lat, lon, label, photo (optional)
- `PhotoMetadata`: id, trace_id, filename, lat, lon, timestamp
- `Package`: id, barcode, status, stop_id, photo, scanned_by

---

## 🧠 AI Features Built-In

- GPT-powered barcode scan routing logic (Too Big → House, Too Small → Mailbox)
- Smart route replay with performance metrics
- AI auto-fill for carrier's next stop prediction (optional module)

---

## 🔄 Deployment

- Can be hosted on **Render.com**, Replit, or as PWA
- Supports **APK bundling** with Cordova or TWA (optional)
- Offline-first compatible: saves and syncs later

---

## 🔧 Your Dev Commands (for Reference)

```powershell
mkdir templates
mkdir templates\admin
mkdir templates\partials
mkdir static\uploads
```
And you’ve been saving every finalized update as a **stage zip**, like:
- `ponyxpress_PHASE2.zip`
- `ponyxpress_STAGE7.zip`
- `ponyxpress_FINAL_MASTER_AI_EMBEDDED.zip`

---

## 🧭 Coordinates for Testing

Your default test address:
**251 Herbert St, Stewart, MN 55385**

---

## 🧰 Final Notes

This markdown contains the full structure, command history, app logic, and roles.

You can feed this into any LLM (like `deepseek-coder`, `codegemma`, or `starcoder2`) locally via **Ollama** or **Continue** in VS Code.

---
