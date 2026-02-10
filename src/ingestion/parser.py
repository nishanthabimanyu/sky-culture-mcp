import json
import os
import glob
from typing import Dict, List, Any

def load_culture(culture_path: str) -> Dict[str, Any]:
    """
    Loads the index.json from a culture directory and extracts constellation data.
    """
    index_path = os.path.join(culture_path, "index.json")
    if not os.path.exists(index_path):
        return None

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {index_path}: {e}")
        return None

    culture_id = data.get("id")
    if not culture_id:
        # Fallback to directory name if ID is missing (though it should be there)
        culture_id = os.path.basename(culture_path)

    constellations_data = []
    
    # Process constellations
    if "constellations" in data:
        for const in data["constellations"]:
            native_name = const.get("common_name", {}).get("native", "")
            english_name = const.get("common_name", {}).get("english", "")
            pronounce = const.get("common_name", {}).get("pronounce", "")
            
            # Use native name as primary key, fallback to english or ID
            name = native_name if native_name else english_name
            if not name:
                 name = const.get("id", "unknown")

            # Extract all unique stars from the lines
            stars = set()
            if "lines" in const:
                for line in const["lines"]:
                    # lines can be list of ints, or mixed with strings like "thin"
                    for item in line:
                        if isinstance(item, int):
                            stars.add(item)
            
            constellations_data.append({
                "id": const.get("id"),
                "name": name,
                "english_name": english_name,
                "native_name": native_name,
                "pronounce": pronounce,
                "stars": list(stars),
                "lines": const.get("lines", [])
            })

    return {
        "culture_id": culture_id,
        "region": data.get("region", "Unknown"),
        "classification": data.get("classification", []),
        "constellations": constellations_data
    }

def main():
    root_dir = r"d:\Sky Cultures\stellarium-skycultures"
    output_file = r"d:\Sky Cultures\sky_culture_engine\data\cultural_library.json"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    library = {}

    # Find all subdirectories
    subdirs = [d for d in glob.glob(os.path.join(root_dir, "*")) if os.path.isdir(d)]

    print(f"Found {len(subdirs)} directories to check.")

    for subdir in subdirs:
        # seemingly some non-culture dirs might exist, load_culture checks for index.json
        culture_data = load_culture(subdir)
        if culture_data:
            culture_id = culture_data["culture_id"]
            library[culture_id] = culture_data
            print(f"Loaded culture: {culture_id} with {len(culture_data['constellations'])} constellations")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(library, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated cultural library with {len(library)} cultures at {output_file}")

if __name__ == "__main__":
    main()
