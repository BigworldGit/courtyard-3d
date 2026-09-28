import subprocess, time

views = ["facade", "door", "west", "east", "wing", "aerial", "approach"]
for v in ["door", "west", "wing", "aerial"]:
    url = f"http://localhost:8088/index.html?view={v}"
    # We can inject JS or load with hash
    out = f"/Users/roy/Documents/workspace/courtyard_3d/render_{v}.png"
    subprocess.run([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new",
        "--window-size=1600,1000",
        f"--screenshot={out}",
        f"http://localhost:8088/index.html#{v}"
    ], capture_output=True)
    print("Captured", v)
