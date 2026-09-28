import subprocess, os, time

views = [
    "facade",
    "door",
    "west_stack",
    "west_annex",
    "east_ladder",
    "east_wing",
    "west_compound",
    "rear_alley",
    "rear_overview",
    "approach"
]

output_dir = "/Users/roy/Documents/workspace/courtyard_3d/renders"
os.makedirs(output_dir, exist_ok=True)

for v in views:
    out = os.path.join(output_dir, f"view_{v}.png")
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new",
        "--enable-webgl",
        "--use-gl=angle",
        "--window-size=1600,1000",
        "--virtual-time-budget=2500",
        f"--screenshot={out}",
        f"http://localhost:8088/index.html#{v}"
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(out):
        print(f"Captured {v}: {os.path.getsize(out)} bytes")
    else:
        print(f"Failed {v}: {res.stderr.decode('utf-8', errors='ignore')}")

print("All captures completed.")
