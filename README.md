# Sky Culture MCP: Archaeoastronomy Computation Engine

## Changing the Lens, Not the Telescope

In my previous work translating the *Surya Siddhanta*, I spent months manually calculating planetary positions to verify ancient Sanskrit verses against modern ephemerides. It was a tedious, repetitive process of building bespoke simulations for a single cultural context.

When I moved on to Mayan and Chinese astronomy for my **Final Year Project**, I realized I was making the same mistake: I was building a new "telescope" (simulation engine) for every culture.

**Sky Culture MCP* was developed as the solution. It serves as the **core computational module** for the broader project, representing a shift in architecture. Instead of rebuilding the telescope, I simply changed the lens.

This modular "Interchangeable Lens" allows AI Agents to abstract the complexity of orbital mechanics. Whether the input is a Mayan Long Count date or a Han Dynasty star name, this microservice handles the physics, allowing the Agent to focus on the cultural interpretation.

## Technical Architecture

This module implements the **Model Context Protocol (MCP)** to expose high-precision astronomical functions to Large Language Models (LLMs) like Claude.

*   **Ephemeris**: NASA JPL DE421 (Covers 1900 BC to 2050 AD).
*   **Physics Engine**: Skyfield (Vector astrometry).
*   **Time Standard**: Barycentric Dynamical Time (TDB).
*   **Standards Compliance**: IAU Working Group on Star Names (WGSN).

## Integration Guide: Claude Desktop

To use this engine as a "Lens" for Claude, you must register it in your `claude_desktop_config.json`.

**Prerequisite**: You must have Docker installed and running.

1.  Locate your configuration file:
    *   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
    *   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

2.  Add the `sky-culture-lite` entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "sky-culture-lite": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "yourname/sky-culture-lite"
      ]
    }
  }
}
```

*Note: Replace `yourname/sky-culture-lite` with your local image tag if you haven't pushed to Docker Hub yet (e.g., `sky-culture-lite`).*

## Exposed Functions

The server exposes the following function signatures to the Model Context Protocol (MCP) host.

### 1. `convert_culture_to_coordinates`

**Signature**: `(culture_id: str, object_name: str, date_str: str) -> str`

This is the primary "Lens" function. It performs the complete translation from a cultural description to a scientific vector.

*   **Inputs**:
    *   `culture_id`: The target cultural context (e.g., `mayan`, `chinese_han`).
    *   `object_name`: The native name of the celestial object (e.g., `chak_ek`, `yinghuo`).
    *   `date_str`: The historical epoch. Supports **Mayan Long Count** (`M:b,k,t,u,k`) and **Julian** (`J:y,m,d`) formats.
*   **Returns**: 
    *   Barycentric Dynamical Time (TDB)
    *   Julian Day Number (JD)
    *   J2000 Right Ascension & Declination (ICRF)

### 2. `list_cultures`

**Signature**: `() -> str`

Returns a catalog of the currently loaded cultural contexts. This allows the Agent to "survey" the available lenses before selecting one.

*   **Returns**: A formatted list of available Culture IDs and their associated celestial objects.

## References

*   **NASA Jet Propulsion Laboratory**: Development Ephemerides (DE421)
*   **International Astronomical Union**: [WGSN Bulletin (Star Names)](https://www.pas.rochester.edu/~emamajek/WGSN/WGSN_bulletin1.pdf)
