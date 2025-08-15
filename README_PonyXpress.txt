# 🐎 PonyXpress: Offline-First Rural Delivery Management System

## Overview
PonyXpress is a full-featured barcode scanning, map-tracing, route-optimized delivery system tailored for postal-style workflows in offline and low-connectivity areas.

## Features
- 📦 Package Scanning + Barcode Labeling
- 🗺️ Interactive Map with Mailbox Stop Placement
- 🚚 Route Tracing + GPS Replay
- 🧾 PDF, CSV, GPX, KML Export
- 🌐 Web + PWA + APK + Desktop App
- 🔒 Role-Based Auth: Carrier, Sub, Admin
- 📤 Cloud Sync, Email Logs, Slack + Zapier
- 📈 Analytics Dashboard + Invoicing
- ⚡ Real-Time WebSockets + AI Chatbot
- 🐳 Docker, Render, GitHub CI, Offline Support
- 📱 Android Launcher + Splash Screen + Camera Overlay
- 🔐 2FA, OAuth, EULA, Privacy, ToS + Localization

## Setup
```bash
# Activate venv
python -m venv .venv
. .venv/Scripts/activate

# Install deps
pip install -r requirements.txt

# Init DB
python -c "from ponyxpress_full_app import db, app; with app.app_context(): db.create_all()"

# Run App
python ponyxpress_full_app.py
```

## Deployment
- Use `render.yaml` for free Render.com cloud hosting
- Use `buildozer.spec` + `main.py` to create Android APK
- Use `pyinstaller_build.ps1` to generate Windows EXE
- Use `docker_compose.yml` for containerized hosting

## Legal
See EULA.txt, PrivacyPolicy.txt, and TermsOfService.txt (multi-language supported).

## Credits
Built with ❤️ by AI + Joshua Rotgers
