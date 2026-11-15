# 🚀 Planet Weight, Age and Breathability Calculator
## A Space Explorer's Guide to the Solar System

A Python desktop application built with **Tkinter**, **ttk**, and **Matplotlib**. It calculates a space explorer's weight, orbital age, and atmospheric breathability across all eight planets of the Solar System based on NASA planetary factsheets.

---

## 🌟 Key Features

- 🌌 **Deep Space Dark Theme**: Custom dark navy and cyan UI design built using Tkinter and TTK.
- 🏋️ **Planetary Weight Calculation**: Converts Earth weight to equivalent surface weight on Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune using standard gravity formulas ($m/s^2$).
- ⏳ **Orbital Age Calculation**: Converts Earth age into local planetary years based on each planet's orbital revolution period around the Sun.
- 🫁 **Atmospheric Breathability Analysis**: Evaluates atmospheric composition and flags breathability based on human physiological oxygen requirements ($19.5\% - 23.5\% \text{ O}_2$).
- 🛰️ **Explorer Survival Summary**: Provides an instant summary of the explorer's heaviest planet, lightest planet, and sole breathable sanctuary.
- 📊 **Matplotlib Visualizations**: Displays comparative bar charts for weight and orbital age (logarithmic scale) across all 8 planets.
- 🛡️ **Robust Validation**: Gracefully handles invalid, non-numeric, negative, or unrealistic inputs with inline visual alerts and no crashes.

---

## 📁 Repository Structure

```
c:/Users/PREETHI/Downloads/sap mini 2/
├── planet_data.py               # NASA planetary constants & data dictionary
├── calculator_logic.py          # Core mathematical logic, validation & summary generators
├── gui_app.py                   # Tkinter/TTK GUI implementation & Matplotlib integration
├── main.py                      # Application entry point launcher
├── test_calculator.py           # Unit tests for calculation & validation logic
├── render_project_screenshots.py# Automated visual screenshot generator
├── sample_output.png            # Application output screenshot
├── sample_input_error.png       # Input validation alert screenshot
├── sample_chart.png             # Matplotlib comparative bar chart screenshot
├── PROJECT_REPORT.md            # Comprehensive project documentation report
└── README.md                    # Project overview and run guide
```

---

## 🚀 How to Run the Application

### Prerequisites
- Python 3.8+ (tested on Python 3.13)
- Required Packages: `matplotlib`, `pillow` (Optional, for visual charts)

```bash
pip install matplotlib pillow
```

### Run Application
```bash
python main.py
```

### Run Unit Tests
```bash
python test_calculator.py
```

---

## 📐 Formulas Used

1. **Weight on Planet ($W_p$)**:
   $$W_p = W_e \times \frac{g_p}{g_e}$$
   *Where $W_e$ is Earth weight, $g_p$ is planet gravity, and $g_e = 9.807 \text{ m/s}^2$.*

2. **Age on Planet ($A_p$)**:
   $$A_p = A_e \times \frac{T_e}{T_p}$$
   *Where $A_e$ is Earth age (years), $T_e = 365.25 \text{ days}$, and $T_p$ is planet orbital period in Earth days.*

3. **Breathability Condition**:
   $$\text{Breathable} = \begin{cases} \text{Yes}, & \text{if } 19.5\% \le \text{Oxygen \%} \le 23.5\% \\ \text{No}, & \text{otherwise} \end{cases}$$

---

## 📄 Documentation
For complete technical details, astronomy background, methodology, and AI tools usage, see [`PROJECT_REPORT.md`](file:///c:/Users/PREETHI/Downloads/sap%20mini%202/PROJECT_REPORT.md).
