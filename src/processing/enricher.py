import json
import os
from typing import Dict, Any, List
from src.physics.engine import PhysicsEngine
from src.temporal.broker import TemporalBroker

class LibraryEnricher:
    """
    Enriches the basic cultural library with:
    1. J2000 RA/Dec for every star (using PhysicsEngine).
    2. JDN for any specific dates (using TemporalBroker).
    """

    def __init__(self, library_path: str, hip_catalog_path: str):
        self.library_path = library_path
        self.engine = PhysicsEngine(hip_csv_path=hip_catalog_path)
        # If catalog not found, engine will warn but we continue (mocking or skipping)
        self.broker = TemporalBroker()

    def load_library(self) -> Dict[str, Any]:
        with open(self.library_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def enrich(self) -> Dict[str, Any]:
        data = self.load_library()
        enriched_data = {}

        print(f"Enriching {len(data)} cultures...")

        for culture_id, culture_info in data.items():
            print(f"Processing {culture_id}...")
            enriched_constellations = []

            for const in culture_info.get("constellations", []):
                # Enrich stars
                enriched_stars = []
                for star_id_obj in const.get("stars", []):
                     # star_id_obj might be int or str
                     try:
                         hip_id = int(star_id_obj)
                         coords = self.engine.get_star_j2000(hip_id)
                         
                         if "error" not in coords:
                             enriched_stars.append(coords)
                         else:
                             # Keep ID but note error
                             enriched_stars.append({"hip": hip_id, "error": coords["error"]})
                     except ValueError:
                         pass # Not a HIP ID

                const["stars_enriched"] = enriched_stars
                enriched_constellations.append(const)

            culture_info["constellations"] = enriched_constellations
            enriched_data[culture_id] = culture_info

        return enriched_data

    def save_library(self, data: Dict[str, Any], output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved enriched library to {output_path}")

if __name__ == "__main__":
    # Paths
    base_dir = r"d:\Sky Cultures\sky_culture_engine"
    input_lib = os.path.join(base_dir, "data", "cultural_library.json")
    output_lib = os.path.join(base_dir, "data", "enriched_cultural_library.json")
    # For now, pointing to a non-existent file will just result in "HIP not found" errors, which is fine for testing structure
    hip_catalog = "hip_main.dat" 

    enricher = LibraryEnricher(input_lib, hip_catalog)
    enriched = enricher.enrich()
    enricher.save_library(enriched, output_lib)
