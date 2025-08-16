from app import app as application

# --- auto-wired by PowerShell: Shipments blueprint ---
try:
    target_app = globals().get("application") or globals().get("app")
    if not target_app:
        print("No Flask app object found to attach shipments blueprint.")
    else:
        if "shipments" not in getattr(target_app, "blueprints", {}):
            shipments_bp = None
            try:
                from models.shipments import bp as shipments_bp
            except Exception as _e1:
                try:
                    from shipments import bp as shipments_bp
                except Exception as _e2:
                    shipments_bp = None
                    print("Shipments blueprint not importable:", _e1, _e2)
            if shipments_bp:
                target_app.register_blueprint(shipments_bp)
                print("Shipments blueprint registered.")
except Exception as _e:
    print("Shipments blueprint registration failed:", _e)
# --- end auto-wire ---
