#!/usr/bin/env python3
"""
HighFreqTrader run script

Usage:
  python run.py
"""

import subprocess
from pathlib import Path
import sys
import threading
import time

root = Path(__file__).parent.resolve()

def run(cmd, cwd=None):
    print(f"\nRunning: {' '.join(str(c) for c in cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def stream_output(pipe, prefix=""):
    """Stream subprocess output line by line in real-time."""
    for line in iter(pipe.readline, b""):
        print(f"{prefix}{line.decode('utf-8').rstrip()}")
    pipe.close()


# -------------------------------------------------
# Build and Run .NET API
# -------------------------------------------------
print("\n=== Building .NET API ===")

dotnet_project = root / "api" / "HighFreqTrader.csproj"
dll_path = root / "api" / "bin" / "Release" / "net9.0" / "HighFreqTrader.dll"

# Build first
run(["dotnet", "build", str(dotnet_project), "-c", "Release"])

print("\n=== Starting .NET API ===")
dotnet_process = subprocess.Popen(
    ["dotnet", str(dll_path)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

threading.Thread(target=stream_output, args=(dotnet_process.stdout, "[API] "), daemon=True).start()
threading.Thread(target=stream_output, args=(dotnet_process.stderr, "[API ERR] "), daemon=True).start()

time.sleep(3)
print("Assuming .NET API is ready after build + startup delay.")


# -------------------------------------------------
# Run C++ WebSocket Server
# -------------------------------------------------
print("\n=== Starting C++ WebSocket Server ===")

engine_dir = root / "engine" / "build"
websocket_server = engine_dir / "Release" / "WebSocketServer.exe"

if not websocket_server.exists():
    print("\nERROR: WebSocketServer.exe not found. Build the project first using build.py.")
    sys.exit(1)

cpp_process = subprocess.Popen(
    [str(websocket_server)],
    cwd=engine_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

threading.Thread(target=stream_output, args=(cpp_process.stdout, "[CPP] "), daemon=True).start()
threading.Thread(target=stream_output, args=(cpp_process.stderr, "[CPP ERR] "), daemon=True).start()


# -------------------------------------------------
# Run Unit / Integration Tests
# -------------------------------------------------
print("\n=== Running Unit + Integration Tests ===")

test_project = root / "tests" / "DotNetTests" / "DotNetTests.csproj"

try:
    test_process = subprocess.Popen(
        [
            "dotnet", "test",
            str(test_project),
            "-c", "Release",
            "--logger", "console;verbosity=detailed"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    threading.Thread(target=stream_output, args=(test_process.stdout, "[TEST] "), daemon=True).start()
    threading.Thread(target=stream_output, args=(test_process.stderr, "[TEST ERR] "), daemon=True).start()

    test_process.wait()
    if test_process.returncode != 0:
        print("\nTests failed. Aborting.")
        sys.exit(1)

except subprocess.CalledProcessError:
    print("\nTests failed. Aborting.")
    sys.exit(1)


try:
    print("\nSystem running. Press Ctrl+C to shut down...")
    cpp_process.wait()
    dotnet_process.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    cpp_process.terminate()
    dotnet_process.terminate()
