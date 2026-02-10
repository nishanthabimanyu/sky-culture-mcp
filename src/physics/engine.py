from skyfield.api import Star, load
from skyfield.data import hipparcos
import pandas as pd
import os
from typing import Dict, Any, Tuple, Optional

class PhysicsEngine:
    """
    Handles astronomical calculations.
    Currently optimized for Star lookups (HIP ID -> J2000 RA/Dec).
    Does NOT load planetary ephemeris (DE4xx) to save space.
    """

    def __init__(self, hip_csv_path: Optional[str] = None):
        self.hip_dataframe = None
        # Default path for downloaded Hipparcos data usually handled by skyfield, 
        # but we can specify a local cache.
        # For now, we will assume standard skyfield loading or local file.
        
        # We'll use a lazy load approach or load if path provided
        if hip_csv_path and os.path.exists(hip_csv_path):
             with load.open(hip_csv_path) as f:
                self.hip_dataframe = hipparcos.load_dataframe(f)

    def load_catalog(self, url_or_path: str = 'hip_main.dat'):
        """
        Loads the Hipparcos catalog.
        If file exists locally, loads it. Else downloads from URL (if supported/allowed).
        """
        try:
            # Skyfield's load() can handle local files if they match the name
            if os.path.exists(url_or_path):
                 with load.open(url_or_path) as f:
                    self.hip_dataframe = hipparcos.load_dataframe(f)
            else:
                # If we were to download:
                # with load.open(hipparcos.URL) as f: ...
                # But we might just want to fail gracefully or Mock for now if no internet
                print(f"Warning: Catalog file {url_or_path} not found. Lookups will fail.")
        except Exception as e:
            print(f"Error loading catalog: {e}")

    def get_star_j2000(self, hip_id: int) -> Dict[str, float]:
        """
        Returns the J2000 RA and Dec for a given HIP ID.
        """
        if self.hip_dataframe is None:
            return {"error": "Catalog not loaded"}

        try:
            if hip_id not in self.hip_dataframe.index:
                 return {"error": f"HIP {hip_id} not found"}
            
            star = Star.from_dataframe(self.hip_dataframe.loc[hip_id])
            
            # Star.ra and Star.dec are Angle objects
            # They are nominally J2000 if from Hipparcos
            
            return {
                "hip": hip_id,
                "ra_hours": star.ra.hours,
                "dec_degrees": star.dec.degrees,
                "ra_str": str(star.ra),
                "dec_str": str(star.dec)
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Test script - requires hip_main.dat typically, or we test with mock
    print("Testing Physics Engine (Star Mode)...")
    
    # Mocking data for test if file missing? 
    # Or just printing setup.
    engine = PhysicsEngine()
    
    # NOTE: You normally need to run `load('hip_main.dat')` or similar.
    # For this environment, we might verify if we can fetch it or if user has it.
    
    print("Engine initialized. Call execute_load() with valid path to use.")
