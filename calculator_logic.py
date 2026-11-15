"""
Calculator Logic Module for Space Explorer's Guide to the Solar System.
Handles input validation, planetary weight/age/breathability calculations,
and survival summary generation.
"""

import math
from planet_data import (
    PLANET_DATA,
    EARTH_GRAVITY,
    EARTH_YEAR_DAYS,
    OXYGEN_MIN_BREATHABLE,
    OXYGEN_MAX_BREATHABLE
)

def validate_inputs(name_raw: str, weight_raw: str, age_raw: str):
    """
    Validates explorer name, weight, and age inputs.
    
    Returns:
        tuple: (is_valid (bool), name (str), weight (float), age (float), error_msg (str))
    """
    # 1. Clean and default name
    name = name_raw.strip() if name_raw and name_raw.strip() else "Explorer"

    # 2. Validate weight
    if not weight_raw or not weight_raw.strip():
        return False, name, 0.0, 0.0, "Please enter your weight on Earth in kg."
    
    try:
        weight = float(weight_raw.strip())
    except ValueError:
        return False, name, 0.0, 0.0, "Weight must be a valid numeric number."
    
    if math.isnan(weight) or math.isinf(weight):
        return False, name, 0.0, 0.0, "Weight cannot be NaN or Infinite."
    
    if weight <= 0:
        return False, name, 0.0, 0.0, "Weight must be a positive number greater than 0 kg."
    
    if weight > 1000:
        return False, name, 0.0, 0.0, "Weight exceeds realistic human maximum (1000 kg)."

    # 3. Validate age
    if not age_raw or not age_raw.strip():
        return False, name, 0.0, 0.0, "Please enter your age on Earth in years."
    
    try:
        age = float(age_raw.strip())
    except ValueError:
        return False, name, 0.0, 0.0, "Age must be a valid numeric number."
    
    if math.isnan(age) or math.isinf(age):
        return False, name, 0.0, 0.0, "Age cannot be NaN or Infinite."
    
    if age <= 0:
        return False, name, 0.0, 0.0, "Age must be a positive number greater than 0 years."
    
    if age > 150:
        return False, name, 0.0, 0.0, "Age exceeds realistic human maximum (150 years)."

    return True, name, weight, age, ""

def calculate_planet_weight(earth_weight: float, surface_gravity: float) -> float:
    """
    Formula: Planet Weight = Earth Weight * Planet Gravity / Earth Gravity
    """
    weight = (earth_weight * surface_gravity) / EARTH_GRAVITY
    return round(weight, 2)

def calculate_planet_age(earth_age: float, orbital_period_days: float) -> float:
    """
    Formula: Planet Age = Earth Age * Earth Year Duration / Planet Year Duration
    """
    age = (earth_age * EARTH_YEAR_DAYS) / orbital_period_days
    return round(age, 2)

def is_atmosphere_breathable(oxygen_pct: float) -> bool:
    """
    Formula: Breathable only if oxygen percentage is between 19.5% and 23.5%.
    """
    return OXYGEN_MIN_BREATHABLE <= oxygen_pct <= OXYGEN_MAX_BREATHABLE

def calculate_all_planets(earth_weight: float, earth_age: float) -> list:
    """
    Calculates metrics for all 8 planets.
    
    Returns a list of dictionaries with calculated planetary data.
    """
    results = []
    for key, pdata in PLANET_DATA.items():
        weight = calculate_planet_weight(earth_weight, pdata["gravity"])
        age = calculate_planet_age(earth_age, pdata["orbital_period_days"])
        breathable = is_atmosphere_breathable(pdata["oxygen_pct"])
        
        results.append({
            "planet_key": key,
            "name": pdata["name"],
            "emoji": pdata["emoji"],
            "weight": weight,
            "age": age,
            "oxygen_pct": pdata["oxygen_pct"],
            "breathable": "Yes" if breathable else "No",
            "is_breathable_bool": breathable,
            "temp_c": pdata["temp_c"],
            "main_gas": pdata["main_gas"],
            "note": pdata["note"]
        })
    return results

def get_survival_summary(name: str, results: list) -> dict:
    """
    Generates a survival summary dictionary highlighting:
    - Heaviest planet
    - Lightest planet
    - Only breathable planet
    - Summary text for explorer
    """
    if not results:
        return {}
        
    heaviest = max(results, key=lambda p: p["weight"])
    lightest = min(results, key=lambda p: p["weight"])
    breathable_list = [p for p in results if p["is_breathable_bool"]]
    breathable_name = breathable_list[0]["name"] if breathable_list else "None"
    
    summary_sentence = (
        f"Greeting Explorer {name}! On {heaviest['name']}, your weight reaches a maximum of "
        f"{heaviest['weight']:.2f} kg, whereas on {lightest['name']}, you feel lightest at "
        f"{lightest['weight']:.2f} kg. Crucially, {breathable_name} is the ONLY planet "
        f"in the Solar System where humans can breathe unaided!"
    )
    
    return {
        "heaviest_planet": heaviest["name"],
        "heaviest_weight": heaviest["weight"],
        "lightest_planet": lightest["name"],
        "lightest_weight": lightest["weight"],
        "breathable_planet": breathable_name,
        "summary_sentence": summary_sentence
    }
