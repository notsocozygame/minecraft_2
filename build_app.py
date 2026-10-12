import os
import subprocess

def build_desktop_exe():
    print("[BUILDER] Packaging Windows / Linux .exe via PyInstaller...")
    # Packages mc2.py and all local python modules into a single standalone executable
    subprocess.run(["pyinstaller", "--noconsole", "--onefile", "app.py"], check=True)
    print("[SUCCESS] Desktop executable generated in dist/app(.exe)!")

def build_android_apk():
    print("[BUILDER] Preparing Buildozer spec for Android APK (.apk)...")
    if not os.path.exists("buildozer.spec"):
        subprocess.run(["buildozer", "init"], check=True)
        print("[INFO] buildozer.spec initialized. Configure app requirements in buildozer.spec and run 'buildozer -v android debug'.")
    else:
        print("[INFO] buildozer.spec already exists. Run 'buildozer -v android debug' to compile your APK for Android & Smartwatches!")

if __name__ == "__main__":
    choice = input("Select build target ([1] Desktop .exe, [2] Android .apk): ")
    if choice == "1":
        build_desktop_exe()
    elif choice == "2":
        build_android_apk()
    else:
        print("Invalid choice.")
