"""
Unit Tests for Space Explorer's Guide to the Solar System.
Tests input validation, mathematical formulas, breathability limits, and summary generation.
"""

import unittest
from calculator_logic import (
    validate_inputs,
    calculate_planet_weight,
    calculate_planet_age,
    is_atmosphere_breathable,
    calculate_all_planets,
    get_survival_summary
)
from planet_data import PLANET_DATA

class TestSpaceExplorerCalculator(unittest.TestCase):

    def test_valid_inputs(self):
        is_valid, name, weight, age, err = validate_inputs("  Alex  ", "70", "25")
        self.assertTrue(is_valid)
        self.assertEqual(name, "Alex")
        self.assertEqual(weight, 70.0)
        self.assertEqual(age, 25.0)
        self.assertEqual(err, "")

    def test_default_name(self):
        is_valid, name, weight, age, err = validate_inputs("", "80.5", "30")
        self.assertTrue(is_valid)
        self.assertEqual(name, "Explorer")

    def test_invalid_weight(self):
        # Empty weight
        valid, _, _, _, err = validate_inputs("Alex", "", "25")
        self.assertFalse(valid)
        self.assertIn("enter your weight", err)

        # String weight
        valid, _, _, _, err = validate_inputs("Alex", "abc", "25")
        self.assertFalse(valid)
        self.assertIn("valid numeric", err)

        # Negative weight
        valid, _, _, _, err = validate_inputs("Alex", "-50", "25")
        self.assertFalse(valid)
        self.assertIn("positive number", err)

        # Zero weight
        valid, _, _, _, err = validate_inputs("Alex", "0", "25")
        self.assertFalse(valid)
        self.assertIn("positive number", err)

        # Unrealistic high weight
        valid, _, _, _, err = validate_inputs("Alex", "1500", "25")
        self.assertFalse(valid)
        self.assertIn("exceeds realistic", err)

    def test_invalid_age(self):
        # Negative age
        valid, _, _, _, err = validate_inputs("Alex", "70", "-5")
        self.assertFalse(valid)
        self.assertIn("positive number", err)

        # Zero age
        valid, _, _, _, err = validate_inputs("Alex", "70", "0")
        self.assertFalse(valid)
        self.assertIn("positive number", err)

        # Unrealistic high age
        valid, _, _, _, err = validate_inputs("Alex", "70", "200")
        self.assertFalse(valid)
        self.assertIn("exceeds realistic", err)

    def test_weight_calculation(self):
        # Earth weight 70 kg on Earth (gravity 9.807) -> 70.0 kg
        w_earth = calculate_planet_weight(70.0, 9.807)
        self.assertAlmostEqual(w_earth, 70.0, places=2)

        # Earth weight 70 kg on Jupiter (gravity 24.79) -> 70 * 24.79 / 9.807 = 176.94
        w_jup = calculate_planet_weight(70.0, 24.79)
        expected_jup = round((70.0 * 24.79) / 9.807, 2)
        self.assertEqual(w_jup, expected_jup)

    def test_age_calculation(self):
        # Earth age 25 on Earth (orbital period 365.25) -> 25.0
        a_earth = calculate_planet_age(25.0, 365.25)
        self.assertAlmostEqual(a_earth, 25.0, places=2)

        # Earth age 25 on Mercury (orbital period 87.97) -> 25 * 365.25 / 87.97 = 103.80
        a_merc = calculate_planet_age(25.0, 87.97)
        expected_merc = round((25.0 * 365.25) / 87.97, 2)
        self.assertEqual(a_merc, expected_merc)

    def test_breathability(self):
        # Earth (20.95%) -> True
        self.assertTrue(is_atmosphere_breathable(20.95))
        # Boundary cases: 19.5% -> True, 23.5% -> True
        self.assertTrue(is_atmosphere_breathable(19.5))
        self.assertTrue(is_atmosphere_breathable(23.5))

        # Outside bounds: Mars (0.13%) -> False, Mercury (42.0%) -> False
        self.assertFalse(is_atmosphere_breathable(0.13))
        self.assertFalse(is_atmosphere_breathable(42.0))
        self.assertFalse(is_atmosphere_breathable(0.0))

    def test_survival_summary(self):
        results = calculate_all_planets(70.0, 25.0)
        summary = get_survival_summary("Commander", results)
        
        self.assertEqual(summary["heaviest_planet"], "Jupiter")
        self.assertEqual(summary["lightest_planet"], "Mercury")
        self.assertEqual(summary["breathable_planet"], "Earth")
        self.assertIn("Commander", summary["summary_sentence"])

if __name__ == "__main__":
    unittest.main()
