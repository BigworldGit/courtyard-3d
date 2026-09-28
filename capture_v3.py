import subprocess, time

views = ["facade", "door", "west", "wing"]
for v in views:
    out = f"/Users/roy/Documents/workspace/courtyard_3d/render_{v}_v3.png"
    subprocess.run([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new",
        "--window-size=1600,1000",
        f"--screenshot={out}",
        f"http://localhost:8088/index.html#{v}"
    ], capture_output=True)
    print("Captured", v)
