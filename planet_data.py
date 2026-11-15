"""
Planet Data Module for Space Explorer's Guide to the Solar System.
Stores physical, orbital, and atmospheric data for all 8 planets based on
NASA Planetary Fact Sheets.
"""

# Earth reference constants
EARTH_GRAVITY = 9.807          # Surface gravity in m/s^2
EARTH_YEAR_DAYS = 365.25       # Orbital period in Earth days
OXYGEN_MIN_BREATHABLE = 19.5   # Minimum oxygen percentage for human respiration
OXYGEN_MAX_BREATHABLE = 23.5   # Maximum oxygen percentage for safe human respiration

# NASA Planetary Data
# Note: For gas giants (Jupiter, Saturn, Uranus, Neptune), values are taken at the 1-bar atmospheric pressure level.
PLANET_DATA = {
    "Mercury": {
        "name": "Mercury",
        "emoji": "☿️",
        "gravity": 3.70,               # m/s^2
        "orbital_period_days": 87.97,  # Earth days
        "oxygen_pct": 42.0,            # % (exosphere trace level, no pressure)
        "main_gas": "Exosphere (Na / He / O2)",
        "temp_c": 167.0,               # Average surface temp °C
        "note": "Extremely thin exosphere; virtually no surface pressure."
    },
    "Venus": {
        "name": "Venus",
        "emoji": "♀️",
        "gravity": 8.87,
        "orbital_period_days": 224.70,
        "oxygen_pct": 0.0,
        "main_gas": "Carbon Dioxide (96.5%)",
        "temp_c": 464.0,
        "note": "Crushing pressure (92 bar) and dense toxic sulfuric clouds."
    },
    "Earth": {
        "name": "Earth",
        "emoji": "🌍",
        "gravity": 9.807,
        "orbital_period_days": 365.25,
        "oxygen_pct": 20.95,
        "main_gas": "Nitrogen (78%) / Oxygen (21%)",
        "temp_c": 15.0,
        "note": "Home planet. Perfectly balanced life-sustaining atmosphere."
    },
    "Mars": {
        "name": "Mars",
        "emoji": "♂️",
        "gravity": 3.71,
        "orbital_period_days": 687.00,
        "oxygen_pct": 0.13,
        "main_gas": "Carbon Dioxide (95.3%)",
        "temp_c": -65.0,
        "note": "Thin atmosphere with trace oxygen; frequent global dust storms."
    },
    "Jupiter": {
        "name": "Jupiter",
        "emoji": "🪐",
        "gravity": 24.79,
        "orbital_period_days": 4332.59, # ~11.86 Earth years
        "oxygen_pct": 0.0,
        "main_gas": "Hydrogen (89.8%) / Helium (10.2%)",
        "temp_c": -110.0,
        "note": "Gas giant with no solid surface; gravity measured at 1-bar pressure level."
    },
    "Saturn": {
        "name": "Saturn",
        "emoji": "🪐",
        "gravity": 10.44,
        "orbital_period_days": 10759.22, # ~29.46 Earth years
        "oxygen_pct": 0.0,
        "main_gas": "Hydrogen (96.3%) / Helium (3.2%)",
        "temp_c": -140.0,
        "note": "Ringed gas giant; low density planet."
    },
    "Uranus": {
        "name": "Uranus",
        "emoji": "🧊",
        "gravity": 8.69,
        "orbital_period_days": 30685.40, # ~84.01 Earth years
        "oxygen_pct": 0.0,
        "main_gas": "Hydrogen (82.5%) / Methane (2.3%)",
        "temp_c": -195.0,
        "note": "Ice giant with extreme axial tilt and freezing atmosphere."
    },
    "Neptune": {
        "name": "Neptune",
        "emoji": "🔵",
        "gravity": 11.15,
        "orbital_period_days": 60189.00, # ~164.79 Earth years
        "oxygen_pct": 0.0,
        "main_gas": "Hydrogen (80%) / Methane (1.5%)",
        "temp_c": -200.0,
        "note": "Outermost ice giant featuring supersonic winds."
    }
}
