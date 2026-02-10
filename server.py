#!/usr/bin/env python3
"""
Sky Culture Lite MCP Server
Transforms cultural sky descriptions into modern coordinates and Stellarium scripts.
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from fastmcp import FastMCP
from skyfield.api import Loader, Topos, Star
from skyfield.data import hipparcos
import convertdate
from convertdate import mayan, julian

# Configure logging to stderr
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stderr)
logger = logging.getLogger("SkyCulture-Lite")

# Initialize MCP Server
mcp = FastMCP("SkyCulture-Lite")

# Load Skyfield Data
load = Loader('data')
try:
    ts = load.timescale()
    # Attempt to load de421.bsp. If explicit path needed, adjust. Usually Loader handles download/cache.
    # Note: In Docker, this requires internet access on first build/run unless volume mounted.
    planets = load('de421.bsp')
    earth = planets['earth']
except Exception as e:
    logger.error(f"Failed to load ephemeris: {e}")
    # Fallback or exit? For now, log error but continue (tools will fail if called)

# Load Cultural Library
CULTURAL_LIBRARY = {}
try:
    with open('cultural_library.json', 'r', encoding='utf-8') as f:
        CULTURAL_LIBRARY = json.load(f)
except FileNotFoundError:
    logger.warning("cultural_library.json not found. Using empty library.")


def parse_ancient_date(date_str: str):
    """
    Parses date strings with prefixes:
    M:b,k,t,u,k -> Mayan Long Count
    J:y,m,d -> Julian Calendar
    ISO -> Gregorian
    Returns: Time object from Skyfield (Julian Day)
    """
    date_str = date_str.strip()
    
    try:
        if date_str.startswith("M:"):
            # Mayan: M:13,0,0,0,0
            parts = [int(x) for x in date_str[2:].split(',')]
            if len(parts) != 5:
                raise ValueError("Mayan date requires 5 components (b,k,t,u,k)")
            jd = mayan.to_jd(*parts)
            return ts.jd(jd)

        elif date_str.startswith("J:"):
            # Julian: J:200,1,1
            parts = [int(x) for x in date_str[2:].split(',')]
            if len(parts) != 3:
                raise ValueError("Julian date requires 3 components (y,m,d)")
            jd = julian.to_jd(*parts)
            return ts.jd(jd)
        
        else:
            # Try ISO format (Gregorian)
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return ts.from_datetime(dt)

    except Exception as e:
        logger.error(f"Date parsing error: {e}")
        raise ValueError(f"Invalid date format: {e}")


@mcp.tool()
def list_cultures() -> str:
    """Returns a list of available cultures and their objects."""
    try:
        lines = ["✅ Available Cultures:"]
        for cid, data in CULTURAL_LIBRARY.items():
            objs = ", ".join(data.get("objects", {}).keys())
            lines.append(f"- {data.get('name')} ({cid}): {objs}")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error listing cultures: {str(e)}"


@mcp.tool()
def convert_culture_to_stellarium(culture_id: str = "", object_name: str = "", date_str: str = "", lat: str = "0", lon: str = "0") -> str:
    """Converts cultural object & date to coords + Stellarium script. Date formats: 'M:13,0,0,0,0', 'J:200,1,1'."""
    if not culture_id or not object_name or not date_str:
        return "❌ Error: culture_id, object_name, and date_str are required"

    try:
        # 1. Lookup Object
        culture_data = CULTURAL_LIBRARY.get(culture_id)
        if not culture_data:
            return f"❌ Error: Culture '{culture_id}' not found"
        
        obj_data = culture_data.get("objects", {}).get(object_name)
        if not obj_data:
            return f"❌ Error: Object '{object_name}' not found in culture '{culture_id}'"
        
        modern_id = obj_data.get("modern_id") # e.g. 'mars', 'venus'
        
        # 2. Parse Date
        t = parse_ancient_date(date_str)
        jd_val = t.tt
        
        # 3. Calculate Position
        observer = earth + Topos(latitude_degrees=float(lat), longitude_degrees=float(lon))
        body = planets[modern_id]
        astrometric = observer.at(t).observe(body)
        ra, dec, distance = astrometric.radec()
        
        ra_str = str(ra)
        dec_str = str(dec)
        
        # 4. Generate Stellarium Script
        script = f"""
// Stellarium Script for {culture_id} - {object_name}
// Date: {date_str} -> JD: {jd_val}
core.setDate("{t.utc_iso()}");
core.selectObjectByName("{modern_id.capitalize()}", true);
core.setObserverLocation({lon}, {lat}, 100, 1, "Earth");
StelMovementMgr.zoomTo(20, 1);
core.output("Loaded {object_name}");
"""

        return f"""✅ Success: {object_name} ({modern_id})
        
**Scientific Data:**
- J2000 RA: {ra_str}
- J2000 Dec: {dec_str}
- Date (UTC): {t.utc_iso()}
- Julian Day: {jd_val:.4f}

**Stellarium Script:**
```javascript
{script.strip()}
```
"""

    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
