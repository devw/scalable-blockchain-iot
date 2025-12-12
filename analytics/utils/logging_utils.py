# analytics/utils/logging_utils.py

def log_info(message: str):
    print(f"[INFO] {message}")

# CSV operations
def log_loading_csv(path: str):
    print(f"📥 Loading CSV: {path}")

def log_csv_loaded(path: str):
    print(f"✅ CSV loaded: {path}")

# Plot / image operations
def log_generating_plot(name: str = ""):
    suffix = f" ({name})" if name else ""
    print(f"🖼️  Generating plot{suffix}...")

def log_saving_plot(path: str):
    print(f"💾 Saving plot to: {path}")

def log_saved_plot(path: str):
    print(f"📤 Plot saved: {path}")

# General-purpose success log
def log_success(message: str):
    print(f"🎉 {message}")
