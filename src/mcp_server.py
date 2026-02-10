import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
import json
from typing import Dict, Any, List, Optional
from src.temporal.broker import TemporalBroker
from src.physics.engine import PhysicsEngine

# Initialize MCP Server
mcp = FastMCP("Sky Culture Engine")

# Global instances
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ENRICHED_LIB_PATH = os.path.join(DATA_DIR, "enriched_cultural_library.json")

# Initialize Logic Modules
broker = TemporalBroker()
CATALOG_PATH = os.getenv("HIP_CATALOG_PATH", os.path.join(DATA_DIR, "hip_main.dat"))
engine = PhysicsEngine(hip_csv_path=CATALOG_PATH)

def load_library():
    if os.path.exists(ENRICHED_LIB_PATH):
        with open(ENRICHED_LIB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

CULTURAL_LIBRARY = load_library()

@mcp.tool()
def list_cultures() -> str:
    """Returns a newline-separated list of all available sky culture IDs."""
    keys = list(CULTURAL_LIBRARY.keys())
    return "✅ Available Cultures:\n" + "\n".join(keys)

@mcp.tool()
def get_culture_details(culture_id: str = "") -> str:
    """Returns the full JSON details for a specific culture as a string."""
    if not culture_id:
        return "❌ Error: culture_id is required"
    
    data = CULTURAL_LIBRARY.get(culture_id)
    if not data:
        return f"❌ Error: Culture '{culture_id}' not found"
        
    return json.dumps(data, indent=2, ensure_ascii=False)

@mcp.tool()
def search_cultural_object(query: str = "") -> str:
    """Searches for stars or constellations by name across all cultures and returns coordinates."""
    if not query:
        return "❌ Error: query string is required"
    
    query = query.lower()
    results = []
    
    for cult_id, data in CULTURAL_LIBRARY.items():
        for const in data.get("constellations", []):
            # Check constellation names
            c_name = const.get("name", "").lower()
            c_eng = const.get("common_name", {}).get("english", "").lower()
            
            if query in c_name or query in c_eng:
                results.append(f"🌌 Constellation: {const.get('name')} ({cult_id})")
                
            # Check stars within constellation
            for star in const.get("stars_enriched", []):
                # star is a dict with hip, ra, dec
                # We don't have star names in the enriched star object (only HIP), 
                # but if the query matches the culture definition we might find it.
                # Currently simple HIP mapping.
                pass

    if not results:
        return f"⚠️ No results found for '{query}'"
        
    return "✅ Search Results:\n" + "\n".join(results[:20])

@mcp.tool()
def convert_date(date_json: str = "", culture: str = "gregorian") -> str:
    """Converts a JSON date string to Julian Day Number (JDN). Format: '{"year": 2023, ...}'"""
    if not date_json:
        return "❌ Error: date_json string is required"
        
    try:
        if isinstance(date_json, str):
            date_dict = json.loads(date_json)
        else:
            return "❌ Error: date_json must be a JSON string"
            
        jdn = broker.to_jdn(date_dict, culture)
        return f"✅ JDN: {jdn}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def get_star_coordinates(hip_id: str = "") -> str:
    """Returns J2000 RA/Dec for a given Hipparcos ID (e.g., '12345')."""
    if not hip_id:
        return "❌ Error: hip_id is required"
        
    try:
        hid = int(hip_id)
        data = engine.get_star_j2000(hid)
        if "error" in data:
            return f"❌ Error: {data['error']}"
        return f"✅ Star HIP {hid}:\nRA: {data['ra_str']}\nDec: {data['dec_str']}"
    except ValueError:
        return f"❌ Error: Invalid HIP ID '{hip_id}'"

@mcp.tool()
def generate_stellarium_script(culture_id: str = "") -> str:
    """Returns the path to a generated Stellarium script for the given culture."""
    if not culture_id:
        return "❌ Error: culture_id is required"

    script_path = os.path.join(BASE_DIR, "scripts", f"load_{culture_id}.ssc")
    if os.path.exists(script_path):
        return f"✅ Script found at: {script_path}"
    else:
        return f"❌ Script not found for '{culture_id}'. Run generation phase."

if __name__ == "__main__":
    # fastmcp run src.mcp_server:mcp
    mcp.run()
