# download_dataset.py
import os
import subprocess
import sys

# If you have a Google Drive file id for a zipped dataset, put it here (optional)
DRIVE_ZIP_ID = ""  # e.g. "1a2B3cD4..."; leave empty if you want to use kaggle

def run(cmd):
    print(">", cmd)
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        raise SystemExit(f"Command failed: {cmd}")

def download_from_kaggle():
    print("Downloading from Kaggle...")
    run("pip install kaggle -q")
    # Assumes user has ~/.kaggle/kaggle.json or uploaded one
    run("kaggle datasets download -d emmarex/plantdisease -f plantdisease.zip -p . --force")
    run("unzip -q plantdisease.zip -d PlantVillage")
    print("Downloaded and extracted to ./PlantVillage")

def download_from_drive():
    if not DRIVE_ZIP_ID:
        print("No Google Drive ID set (DRIVE_ZIP_ID). Cannot download from Drive.")
        return
    print("Downloading zip from Google Drive...")
    run("pip install gdown -q")
    cmd = f"gdown --id {DRIVE_ZIP_ID} -O plantdisease.zip"
    run(cmd)
    run("unzip -q plantdisease.zip -d PlantVillage")
    print("Downloaded and extracted to ./PlantVillage")

if __name__ == "__main__":
    # Prefer kaggle if available
    if os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")):
        try:
            download_from_kaggle()
        except Exception as e:
            print("Kaggle download failed:", e)
            if DRIVE_ZIP_ID:
                download_from_drive()
            else:
                print("Set DRIVE_ZIP_ID to use Drive fallback.")
    else:
        print("~/.kaggle/kaggle.json not found.")
        if DRIVE_ZIP_ID:
            download_from_drive()
        else:
            print("Upload kaggle.json (or set DRIVE_ZIP_ID) then re-run.")
