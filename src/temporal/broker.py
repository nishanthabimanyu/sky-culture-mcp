import convertdate
from convertdate import julian, mayan, gregorian
from typing import Union, List, Tuple, Dict, Optional, Any
import datetime
import re

class TemporalBroker:
    """
    Handles conversion of various cultural dates to Julian Day Numbers (JDN).
    Supports uncertainty by returning ranges (sweeps).
    """

    # Epoch for Egyptian Civil Calendar: Feb 26, 747 BCE (Julian) = JDN 1448638
    EGYPTIAN_EPOCH = 1448638.0

    def __init__(self):
        pass

    def to_jdn(self, date_input: Dict[str, Any], culture: str = "western") -> Union[float, Tuple[float, float]]:
        """
        Converts a date input dictionary to JDN.
        
        Args:
            date_input: Dictionary containing date components.
                        Examples:
                        - Mayan: {"baktun": 13, "katun": 0, "tun": 0, "winal": 0, "kin": 0}
                        - Egyptian: {"year": 1, "month": 1, "day": 1}
                        - Julian: {"year": 2023, "month": 1, "day": 1}
                        - Range: {"start": {...}, "end": {...}}
            culture: The cultural context ("mayan", "egyptian", "julian", "gregorian")

        Returns:
            float: Single JDN for specific dates.
            Tuple[float, float]: (start_jdn, end_jdn) for ranges.
        """
        if "start" in date_input and "end" in date_input:
            start_jdn = self._convert_single(date_input["start"], culture)
            end_jdn = self._convert_single(date_input["end"], culture)
            return (start_jdn, end_jdn)
        
        return self._convert_single(date_input, culture)

    def _convert_single(self, components: Dict[str, int], culture: str) -> float:
        """Helper to convert a single date object."""
        culture = culture.lower()
        
        try:
            if culture == "mayan":
                return mayan.to_jd(
                    components.get("baktun", 0),
                    components.get("katun", 0),
                    components.get("tun", 0),
                    components.get("winal", 0),
                    components.get("kin", 0)
                )
            
            elif culture == "egyptian":
                return self._egyptian_to_jd(
                    components.get("year", 1),
                    components.get("month", 1),
                    components.get("day", 1)
                )
            
            elif culture == "julian":
                return julian.to_jd(
                    components.get("year", 1),
                    components.get("month", 1),
                    components.get("day", 1)
                )
                
            elif culture == "gregorian":
                return gregorian.to_jd(
                    components.get("year", 1),
                    components.get("month", 1),
                    components.get("day", 1)
                )

            else:
                raise ValueError(f"Unsupported culture: {culture}")

        except Exception as e:
            raise ValueError(f"Date conversion error for {culture} with {components}: {str(e)}")

    def _egyptian_to_jd(self, year: int, month: int, day: int) -> float:
        """
        Converts Egyptian Civil dates to Julian Day Number.
        Epoch: 1 Thoth, 1 Nabonassar = Feb 26, 747 BCE (ISO -746) = JDN 1448638
        """
        # (Year - 1) * 365 + (Month - 1) * 30 + (Day - 1)
        # Note: Egyptian years are simple 365 days, no leap years.
        if month < 1 or month > 13:
            raise ValueError("Egyptian month must be between 1 and 13 (Epagomenal days)")
        if day < 1 or day > 30:
            if month == 13 and day > 5:
                raise ValueError("Epagomenal days are only 5")
            elif month < 13:
                 pass # Standard limits apply but we can be lenient or strict
        
        days_passed = (year - 1) * 365 + (month - 1) * 30 + (day - 1)
        return self.EGYPTIAN_EPOCH + days_passed

if __name__ == "__main__":
    broker = TemporalBroker()
    
    # Test Mayan: 13.0.0.0.0 (Dec 21, 2012)
    # 21 Dec 2012 gregorian is 2456282.5
    mayan_date = {"baktun": 13, "katun": 0, "tun": 0, "winal": 0, "kin": 0}
    jdn = broker.to_jdn(mayan_date, "mayan")
    print(f"Mayan 13.0.0.0.0 JDN: {jdn}")

    # Test Julian
    julian_date = {"year": 208, "month": 1, "day": 1}
    jdn_jul = broker.to_jdn(julian_date, "julian")
    print(f"Julian 208-01-01 JDN: {jdn_jul}")

    # Test Egyptian
    # 1 Thoth, Year 1 = 1448638.0
    eg_date = {"year": 1, "month": 1, "day": 1}
    jdn_eg = broker.to_jdn(eg_date, "egyptian")
    print(f"Egyptian 1-1-1 JDN: {jdn_eg}")
