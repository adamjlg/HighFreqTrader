# HighFreqTrader
Lock-Free High Throughput Trading Engine built with .NET and C++.

## Features
- Lock-free SPSC queue for high throughput
- ASP.NET Core API for submitting orders
- C++ trading engine integrated via C++/CLI
- Order generator for simulation
- Dockerized for easy deployment

## Architecture
See docs/architecture.md for diagrams.

## Running
1. Build engine via CMake
2. Build API via dotnet
3. Run Docker container or locally
4. Use order-generator to simulate order