from app import app as application

# --- auto-wired by PowerShell: Shipments blueprint ---
try:
    from models.shipments import bp as shipments_bp
    target_app = globals().get("application") or globals().get("app")
    if target_app:
        target_app.register_blueprint(shipments_bp)
    else:
        print("No Flask app object found to attach shipments blueprint.")
except Exception as _e:
    print("Shipments blueprint registration failed:", _e)
# --- end auto-wire ---
