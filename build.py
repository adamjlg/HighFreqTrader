#!/usr/bin/env python3
"""
HighFreqTrader build script

Usage:
  python build.py
"""

import subprocess
from pathlib import Path
import shutil
import sys

root = Path(__file__).parent.resolve()

# -------------------------------------------------
# install requests for run.py
# -------------------------------------------------
try:
    import requests
except ImportError:
    print("\n'requests' not found. Installing via pip...")
    subprocess.run([sys.executable, "-m", "pip", "install","--user", "requests"], check=True)
    import requests

vcpkg_dir = root / "vcpkg"
vcpkg_exe = vcpkg_dir / "vcpkg.exe"
vcpkg_toolchain = vcpkg_dir / "scripts/buildsystems/vcpkg.cmake"

engine_dir = root / "engine"
build_dir = engine_dir / "build"


def run(cmd, cwd=None):
    print(f"\nRunning: {' '.join(str(c) for c in cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

# -------------------------------------------------
# Setup vcpkg
# -------------------------------------------------
print("\n=== Setting up vcpkg ===")

if not vcpkg_dir.exists():
    run(["git", "clone", "https://github.com/microsoft/vcpkg"], cwd=root)

if not vcpkg_exe.exists():
    run([str(vcpkg_dir / "bootstrap-vcpkg.bat")], cwd=vcpkg_dir)

# -------------------------------------------------
# Install Boost
# -------------------------------------------------
print("\n=== Installing Boost (system + beast) ===")

run([
    str(vcpkg_exe),
    "install",
    "boost-system:x64-windows",
    "boost-beast:x64-windows",
    "nlohmann-json:x64-windows"
])

# -------------------------------------------------
# Build C++ Engine + WebSocketServer
# -------------------------------------------------
print("\n=== Building C++ Engine + WebSocketServer ===")

if build_dir.exists():
    shutil.rmtree(build_dir)

build_dir.mkdir()

run([
    "cmake",
    "..",
    "-G", "Visual Studio 17 2022",
    "-A", "x64",
    f"-DCMAKE_TOOLCHAIN_FILE={vcpkg_toolchain}"
], cwd=build_dir)

run([
    "cmake",
    "--build", ".",
    "--config", "Release"
], cwd=build_dir)

# -------------------------------------------------
# Build .NET 
# -------------------------------------------------
print("\n=== Building .NET projects ===")

dotnet_projects = [
    root / "api" / "HighFreqTrader.csproj",
    root / "tests" / "DotNetTests" / "DotNetTests.csproj"
]

for project in dotnet_projects:
    run(["dotnet", "build", str(project), "-c", "Release"])

print("\n=== Build Complete ===")
