# 🌌 Sky Culture Lite: Archaeoastronomy Computation Engine

> **Final Year Project Module**: Computational Core for Ancient Sky Simulation

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Docker](https://img.shields.io/badge/docker-containerized-blue.svg)](https://www.docker.com/)
[![MCP](https://img.shields.io/badge/MCP-fastmcp-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Project Overview

**Sky Culture Lite** is a high-precision archaeoastronomy engine designed as a **Microservice Module** for my Final Year Project. It serves as the bridge between ancient cultural astronomical descriptions and modern scientific coordinates.

This engine leverages **NASA's JPL Ephemeris (DE421)** and **Skyfield** to compute planetary positions for any historical epoch (e.g., Mayan Long Count dates, Ancient Egyptian calendars) and translates them into **J2000 Coordinates** and **Stellarium Scripts** for visualization.

### 🚀 Key Features
- **Agentic AI Integration**: Built with the **Model Context Protocol (MCP)** to empower AI agents with astronomical calculation capabilities.
- **High-Precision Physics**: Uses `de421.bsp` (17MB) for accurate planetary positions from 1900 BC to 2050 AD.
- **Multi-Cultural Calendar Support**:
  - **Mayan Long Count** (`M:b,k,t,u,k`) -> Modern Date
  - **Julian/Gregorian** (`J:y,m,d`) -> Modern Date
- **Stellarium Automation**: Generates verified `.ssc` scripting logic for astronomical simulation.

## 🛠️ Technology Stack
- **Core Logic**: Python 3.11
- **Orbital Mechanics**: `skyfield`, `numpy`
- **Calendar Math**: `convertdate`
- **API Protocol**: `fastmcp` (Model Context Protocol)
- **Deployment**: Docker (Slim image, non-root security)

## 📦 Installation & Usage

### 1. Docker (Recommended)
```bash
docker build -t sky-culture-lite .
docker run -i --rm sky-culture-lite
```

### 2. Local Python
```bash
pip install -r requirements.txt
python server.py
# Note: First run will download approx 17MB of ephemeris data.
```

## 🧩 Module Interaction (MCP Tools)

#### `convert_culture_to_stellarium`
The primary tool exposed to the AI Agent. It takes a vague cultural description and returns hard scientific data.

```python
# Example: "Where was the Great Star (Chak Ek) on Mayan Date 9.10.0.0.0?"
convert_culture_to_stellarium(
    culture_id="mayan",
    object_name="chak_ek",
    date_str="M:9,10,0,0,0"
)
```

**Returns:**
- **Scientific Data**: RA/Dec (J2000), Julian Day Number.
- **Stellarium Script**: Code block to visualize the exact alignment.

---
*Developed by Nishanth Abimanyu as part of the Final Year Computer Science Project.*
