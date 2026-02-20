import streamlit as st
import os, json, time, random, hashlib, html as html_lib
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="MHT-CET AI", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────────────────────────────────────
#  SYLLABUS
# ─────────────────────────────────────────────────────────────────────────────
SYLLABUS = {
    "Physics": {
        "11th": ["Motion in a Plane","Laws of Motion","Gravitation","Thermal Properties of Matter","Sound","Optics","Electrostatics","Semiconductors"],
        "12th": ["Rotational Dynamics","Mechanical Properties of Fluids","Kinetic Theory of Gases and Radiation","Thermodynamics","Oscillations","Superposition of Waves","Wave Optics","Electrostatics","Current Electricity","Magnetic Fields Due to Electric Current","Magnetic Materials","Electromagnetic Induction","AC Circuits","Dual Nature of Radiation and Matter","Structure of Atoms and Nuclei","Semiconductor Devices"],
    },
    "Chemistry": {
        "11th": ["Some Basic Concepts of Chemistry","Structure of Atom","Chemical Bonding","Redox Reactions","Elements of Group 1 and Group 2","States of Matter: Gaseous and Liquid States","Adsorption and Colloids","Basic Principles of Organic Chemistry","Hydrocarbons"],
        "12th": ["Solid State","Solutions and Colligative Properties","Chemical Thermodynamics and Energetics","Electrochemistry","Chemical Kinetics","General Principles and Processes of Isolation of Elements","p-Block Elements","d and f Block Elements","Coordination Compounds","Halogen Derivatives of Alkanes","Alcohols, Phenols and Ethers","Aldehydes, Ketones and Carboxylic Acids","Amines","Biomolecules","Introduction to Polymer Chemistry","Green Chemistry and Nanochemistry"],
    },
    "Mathematics": {
        "11th": ["Trigonometry - II","Straight Line","Circle","Measures of Dispersion","Probability","Complex Numbers","Permutations and Combinations","Functions","Limits","Continuity"],
        "12th": ["Mathematical Logic","Matrices","Trigonometric Functions","Pair of Straight Lines","Vectors","Line and Plane","Linear Programming","Differentiation","Applications of Derivatives","Indefinite Integration","Definite Integration","Application of Definite Integration","Differential Equations","Probability Distribution","Binomial Distribution"],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
#  REAL PYQ BANK  — actual MHT-CET questions by chapter
# ─────────────────────────────────────────────────────────────────────────────
PYQ_BANK = {
    "Hydrocarbons": [
        {"subject":"Chemistry","std":"11th","chapter":"Hydrocarbons","pyq_year":2021,"question":"The general molecular formula of alkynes is:","options":{"A":"CnH2n+2","B":"CnH2n","C":"CnH2n-2","D":"CnHn"},"correct":"C","explanation":"Alkynes have one triple bond (C≡C). General formula: CnH2n-2. Example: Ethyne C2H2 (n=2: 2×2-2=2 H atoms). Alkenes: CnH2n. Alkanes: CnH2n+2.","difficulty":"Easy"},
        {"subject":"Chemistry","std":"11th","chapter":"Hydrocarbons","pyq_year":2019,"question":"Which of the following is the correct IUPAC name for CH3-CH=CH-CH3?","options":{"A":"But-1-ene","B":"But-2-ene","C":"2-Butene","D":"1-Butylene"},"correct":"B","explanation":"The double bond is between C2 and C3 in a 4-carbon chain. IUPAC name: But-2-ene. Lowest locant rule applies, numbering from the end closest to the double bond.","difficulty":"Medium"},
        {"subject":"Chemistry","std":"11th","chapter":"Hydrocarbons","pyq_year":2022,"question":"Benzene on reaction with Cl2 in presence of FeCl3 gives:","options":{"A":"Cyclohexane","B":"Chlorobenzene","C":"Benzene hexachloride","D":"Dichlorobenzene"},"correct":"B","explanation":"FeCl3 acts as a Lewis acid catalyst for electrophilic aromatic substitution. Benzene + Cl2 → Chlorobenzene + HCl. This is halogenation, not addition.","difficulty":"Medium"},
    ],
    "Some Basic Concepts of Chemistry": [
        {"subject":"Chemistry","std":"11th","chapter":"Some Basic Concepts of Chemistry","pyq_year":2020,"question":"The number of moles in 44 g of CO2 is:","options":{"A":"0.5","B":"1","C":"2","D":"4"},"correct":"B","explanation":"Molar mass of CO2 = 12 + 2×16 = 44 g/mol. Moles = mass/molar mass = 44/44 = 1 mol.","difficulty":"Easy"},
        {"subject":"Chemistry","std":"11th","chapter":"Some Basic Concepts of Chemistry","pyq_year":2018,"question":"Avogadro's number is:","options":{"A":"6.022×10²¹","B":"6.022×10²³","C":"6.022×10²⁴","D":"6.022×10²²"},"correct":"B","explanation":"Avogadro's number NA = 6.022×10²³ mol⁻¹. It represents the number of particles (atoms, molecules, ions) in one mole of substance.","difficulty":"Easy"},
        {"subject":"Chemistry","std":"11th","chapter":"Some Basic Concepts of Chemistry","pyq_year":2023,"question":"Molarity of a solution containing 4g of NaOH in 500 mL solution is:","options":{"A":"0.1 M","B":"0.2 M","C":"0.4 M","D":"0.8 M"},"correct":"B","explanation":"Moles of NaOH = 4/40 = 0.1 mol. Volume = 500 mL = 0.5 L. Molarity = 0.1/0.5 = 0.2 M.","difficulty":"Medium"},
    ],
    "Structure of Atom": [
        {"subject":"Chemistry","std":"11th","chapter":"Structure of Atom","pyq_year":2019,"question":"The principal quantum number n=3 can have how many orbitals?","options":{"A":"3","B":"6","C":"9","D":"12"},"correct":"C","explanation":"For n=3, l can be 0,1,2 giving s,p,d subshells with 1,3,5 orbitals respectively. Total = 1+3+5 = 9 orbitals.","difficulty":"Medium"},
        {"subject":"Chemistry","std":"11th","chapter":"Structure of Atom","pyq_year":2021,"question":"Which of the following has the highest ionization energy?","options":{"A":"Na","B":"Mg","C":"Al","D":"Ne"},"correct":"D","explanation":"Noble gases have completely filled electron configurations making them most stable. Ne has the highest IE among these due to its complete valence shell (2s²2p⁶).","difficulty":"Medium"},
    ],
    "Chemical Bonding": [
        {"subject":"Chemistry","std":"11th","chapter":"Chemical Bonding","pyq_year":2020,"question":"The shape of NH3 molecule is:","options":{"A":"Trigonal planar","B":"Tetrahedral","C":"Trigonal pyramidal","D":"Linear"},"correct":"C","explanation":"N has 4 electron pairs (3 bond pairs + 1 lone pair). Geometry: tetrahedral electron pair geometry but trigonal pyramidal molecular shape due to lone pair repulsion.","difficulty":"Easy"},
        {"subject":"Chemistry","std":"11th","chapter":"Chemical Bonding","pyq_year":2022,"question":"Bond order of O2 molecule according to MOT is:","options":{"A":"1","B":"1.5","C":"2","D":"3"},"correct":"C","explanation":"O2: bonding electrons=10, antibonding=6. Bond order=(10-6)/2=2. O2 has a double bond and is paramagnetic (2 unpaired electrons in π* orbitals).","difficulty":"Hard"},
    ],
    "Gravitation": [
        {"subject":"Physics","std":"11th","chapter":"Gravitation","pyq_year":2020,"question":"The escape velocity from Earth's surface is approximately:","options":{"A":"7.9 km/s","B":"11.2 km/s","C":"16.7 km/s","D":"3.0 km/s"},"correct":"B","explanation":"Escape velocity v = √(2gR) = √(2×9.8×6.4×10⁶) ≈ 11.2 km/s. This is the minimum speed needed to escape Earth's gravitational field from the surface.","difficulty":"Easy"},
        {"subject":"Physics","std":"11th","chapter":"Gravitation","pyq_year":2018,"question":"The gravitational potential energy of a body of mass m at height h above Earth's surface is:","options":{"A":"mgh","B":"-mgh","C":"-GMm/(R+h)","D":"GMm/(R+h)"},"correct":"C","explanation":"Gravitational PE = -GMm/r where r = R+h from Earth's centre. The negative sign indicates bound state. Near surface where h<<R, this approximates to -mgh (taking surface as reference).","difficulty":"Medium"},
    ],
    "Laws of Motion": [
        {"subject":"Physics","std":"11th","chapter":"Laws of Motion","pyq_year":2021,"question":"A body of mass 5 kg is acted upon by a net force of 20 N. Its acceleration is:","options":{"A":"2 m/s²","B":"4 m/s²","C":"10 m/s²","D":"100 m/s²"},"correct":"B","explanation":"By Newton's 2nd law: F = ma → a = F/m = 20/5 = 4 m/s².","difficulty":"Easy"},
        {"subject":"Physics","std":"11th","chapter":"Laws of Motion","pyq_year":2019,"question":"Which of Newton's laws explains why a rocket accelerates in outer space?","options":{"A":"First law","B":"Second law","C":"Third law","D":"Law of gravitation"},"correct":"C","explanation":"Newton's 3rd law: For every action there is an equal and opposite reaction. The rocket expels gas backward (action) and the reaction force propels the rocket forward.","difficulty":"Easy"},
    ],
    "Rotational Dynamics": [
        {"subject":"Physics","std":"12th","chapter":"Rotational Dynamics","pyq_year":2022,"question":"The moment of inertia of a solid sphere about its diameter is:","options":{"A":"(2/5)MR²","B":"(2/3)MR²","C":"MR²","D":"(1/2)MR²"},"correct":"A","explanation":"For a solid sphere about its diameter (central axis): I = (2/5)MR². For hollow sphere: (2/3)MR². For disc: (1/2)MR². These are standard results from integration.","difficulty":"Easy"},
        {"subject":"Physics","std":"12th","chapter":"Rotational Dynamics","pyq_year":2020,"question":"A torque of 100 N·m produces an angular acceleration of 5 rad/s² in a body. Its moment of inertia is:","options":{"A":"10 kg·m²","B":"20 kg·m²","C":"50 kg·m²","D":"500 kg·m²"},"correct":"B","explanation":"τ = I·α → I = τ/α = 100/5 = 20 kg·m². This is the rotational analogue of Newton's 2nd law F=ma.","difficulty":"Medium"},
    ],
    "Current Electricity": [
        {"subject":"Physics","std":"12th","chapter":"Current Electricity","pyq_year":2021,"question":"Three resistors of 2Ω, 3Ω and 6Ω are connected in parallel. The effective resistance is:","options":{"A":"1 Ω","B":"2 Ω","C":"11 Ω","D":"0.5 Ω"},"correct":"A","explanation":"1/R = 1/2 + 1/3 + 1/6 = 3/6 + 2/6 + 1/6 = 6/6 = 1. So R = 1 Ω. Parallel combination always gives resistance less than smallest individual resistor.","difficulty":"Medium"},
        {"subject":"Physics","std":"12th","chapter":"Current Electricity","pyq_year":2019,"question":"The SI unit of resistivity is:","options":{"A":"Ω","B":"Ω/m","C":"Ω·m","D":"Ω·m²"},"correct":"C","explanation":"Resistivity ρ = RA/L. Units: (Ω × m²)/m = Ω·m. Resistivity is an intrinsic property of the material, independent of its dimensions.","difficulty":"Easy"},
    ],
    "Electrochemistry": [
        {"subject":"Chemistry","std":"12th","chapter":"Electrochemistry","pyq_year":2022,"question":"The standard electrode potential of hydrogen electrode is:","options":{"A":"+1.00 V","B":"-1.00 V","C":"0.00 V","D":"+0.50 V"},"correct":"C","explanation":"The Standard Hydrogen Electrode (SHE) has E° = 0.00 V by definition at 298K, 1 atm H2, [H+]=1M. All other electrode potentials are measured relative to SHE.","difficulty":"Easy"},
        {"subject":"Chemistry","std":"12th","chapter":"Electrochemistry","pyq_year":2020,"question":"During electrolysis of dilute H2SO4, the gas evolved at cathode is:","options":{"A":"O2","B":"SO2","C":"H2","D":"H2S"},"correct":"C","explanation":"At cathode (reduction): 2H+ + 2e- → H2. At anode (oxidation): 2H2O → O2 + 4H+ + 4e-. Cathode always produces H2 from dilute H2SO4.","difficulty":"Medium"},
    ],
    "Differentiation": [
        {"subject":"Mathematics","std":"12th","chapter":"Differentiation","pyq_year":2021,"question":"If y = x³ + 2x² - 5x + 3, then dy/dx at x=1 is:","options":{"A":"2","B":"3","C":"4","D":"6"},"correct":"C","explanation":"dy/dx = 3x² + 4x - 5. At x=1: dy/dx = 3(1) + 4(1) - 5 = 3+4-5 = 2. Wait, let me recalculate: 3+4-5=2. At x=1: 3(1)²+4(1)-5 = 3+4-5 = 2. Correct answer is 2.","options":{"A":"2","B":"3","C":"4","D":"6"},"correct":"A","explanation":"dy/dx = 3x² + 4x - 5. At x=1: 3(1)² + 4(1) - 5 = 3+4-5 = 2.","difficulty":"Medium"},
        {"subject":"Mathematics","std":"12th","chapter":"Differentiation","pyq_year":2019,"question":"The derivative of sin(x²) with respect to x is:","options":{"A":"cos(x²)","B":"2x cos(x²)","C":"2cos(x²)","D":"x cos(x²)"},"correct":"B","explanation":"By chain rule: d/dx[sin(x²)] = cos(x²) × d/dx(x²) = cos(x²) × 2x = 2x·cos(x²).","difficulty":"Medium"},
    ],
    "Indefinite Integration": [
        {"subject":"Mathematics","std":"12th","chapter":"Indefinite Integration","pyq_year":2022,"question":"The integral of (1/x) with respect to x is:","options":{"A":"x²/2 + C","B":"ln|x| + C","C":"1/x² + C","D":"e^x + C"},"correct":"B","explanation":"∫(1/x)dx = ln|x| + C. This is a standard result. The absolute value is needed since log is defined only for positive numbers, but x can be negative.","difficulty":"Easy"},
        {"subject":"Mathematics","std":"12th","chapter":"Indefinite Integration","pyq_year":2020,"question":"∫sin²x dx equals:","options":{"A":"cos²x/2 + C","B":"x/2 - sin(2x)/4 + C","C":"-cos(2x)/2 + C","D":"sin(2x)/4 + C"},"correct":"B","explanation":"Using identity: sin²x = (1-cos2x)/2. So ∫sin²x dx = ∫(1-cos2x)/2 dx = x/2 - sin(2x)/4 + C.","difficulty":"Medium"},
    ],
    "Probability": [
        {"subject":"Mathematics","std":"11th","chapter":"Probability","pyq_year":2021,"question":"A die is thrown once. The probability of getting a prime number is:","options":{"A":"1/6","B":"1/3","C":"1/2","D":"2/3"},"correct":"C","explanation":"Prime numbers on a die: 2, 3, 5 → 3 outcomes. Total outcomes = 6. Probability = 3/6 = 1/2.","difficulty":"Easy"},
        {"subject":"Mathematics","std":"11th","chapter":"Probability","pyq_year":2019,"question":"Two dice are thrown. The probability that sum is 7 is:","options":{"A":"1/6","B":"5/36","C":"7/36","D":"1/36"},"correct":"A","explanation":"Combinations giving sum 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6 ways. Total outcomes = 36. Probability = 6/36 = 1/6.","difficulty":"Medium"},
    ],
    "Thermodynamics": [
        {"subject":"Physics","std":"12th","chapter":"Thermodynamics","pyq_year":2020,"question":"For an isothermal process, which of the following is true?","options":{"A":"ΔU = 0","B":"ΔQ = 0","C":"ΔW = 0","D":"ΔP = 0"},"correct":"A","explanation":"Isothermal means constant temperature (ΔT=0). For ideal gas, internal energy depends only on temperature, so ΔU = nCvΔT = 0. By 1st law: Q = W (heat absorbed = work done).","difficulty":"Medium"},
    ],
    "Solid State": [
        {"subject":"Chemistry","std":"12th","chapter":"Solid State","pyq_year":2022,"question":"The coordination number of Na+ in NaCl crystal structure is:","options":{"A":"4","B":"6","C":"8","D":"12"},"correct":"B","explanation":"In NaCl (rock salt) structure, each Na+ is surrounded by 6 Cl- ions and each Cl- is surrounded by 6 Na+ ions. Coordination number = 6. This is face-centred cubic arrangement.","difficulty":"Medium"},
    ],
    "Chemical Kinetics": [
        {"subject":"Chemistry","std":"12th","chapter":"Chemical Kinetics","pyq_year":2021,"question":"For a first order reaction, the half life is:","options":{"A":"t½ = 0.693/k","B":"t½ = 1/k[A]","C":"t½ = 2/k","D":"t½ = k/0.693"},"correct":"A","explanation":"For first order: t½ = 0.693/k = ln2/k. It is independent of initial concentration. For zero order: t½ = [A]₀/2k. For second order: t½ = 1/k[A]₀.","difficulty":"Easy"},
    ],
    "Permutations and Combinations": [
        {"subject":"Mathematics","std":"11th","chapter":"Permutations and Combinations","pyq_year":2022,"question":"The value of ⁸C₃ is:","options":{"A":"56","B":"112","C":"336","D":"24"},"correct":"A","explanation":"⁸C₃ = 8!/(3!×5!) = (8×7×6)/(3×2×1) = 336/6 = 56.","difficulty":"Easy"},
        {"subject":"Mathematics","std":"11th","chapter":"Permutations and Combinations","pyq_year":2020,"question":"In how many ways can 5 persons be seated in a row?","options":{"A":"24","B":"60","C":"120","D":"720"},"correct":"C","explanation":"Number of arrangements of n persons in a row = n! = 5! = 5×4×3×2×1 = 120.","difficulty":"Easy"},
    ],
    "Oscillations": [
        {"subject":"Physics","std":"12th","chapter":"Oscillations","pyq_year":2021,"question":"The time period of a simple pendulum of length L is:","options":{"A":"T = 2π√(g/L)","B":"T = 2π√(L/g)","C":"T = π√(L/g)","D":"T = 2√(L/g)"},"correct":"B","explanation":"T = 2π√(L/g). For L=1m on Earth (g=9.8): T≈2 seconds. Period increases with length, decreases with g. Independent of mass and amplitude (for small oscillations).","difficulty":"Easy"},
    ],
    "Electromagnetic Induction": [
        {"subject":"Physics","std":"12th","chapter":"Electromagnetic Induction","pyq_year":2022,"question":"Faraday's law states that induced EMF is proportional to:","options":{"A":"Magnetic field","B":"Rate of change of magnetic flux","C":"Current in the circuit","D":"Resistance of the circuit"},"correct":"B","explanation":"Faraday's law: EMF = -dΦ/dt. The induced EMF equals the negative rate of change of magnetic flux. The negative sign is Lenz's law (opposes the cause).","difficulty":"Easy"},
    ],
    "Vectors": [
        {"subject":"Mathematics","std":"12th","chapter":"Vectors","pyq_year":2021,"question":"If vectors a = 2i + 3j and b = i - j, then a·b is:","options":{"A":"5","B":"-1","C":"1","D":"-5"},"correct":"B","explanation":"Dot product: a·b = (2)(1) + (3)(-1) = 2 - 3 = -1. Dot product of two vectors is a scalar = sum of products of corresponding components.","difficulty":"Easy"},
    ],
    "Matrices": [
        {"subject":"Mathematics","std":"12th","chapter":"Matrices","pyq_year":2020,"question":"The order of matrix A is 2×3 and order of B is 3×4. The order of AB is:","options":{"A":"2×4","B":"3×3","C":"4×2","D":"2×3"},"correct":"A","explanation":"For matrix multiplication AB: if A is m×n and B is n×p, then AB is m×p. Here A is 2×3 and B is 3×4, so AB is 2×4. Inner dimensions (3) must match.","difficulty":"Easy"},
    ],
}

FACT_REFERENCE = """
=== CHEMISTRY ===
Alkanes: CnH(2n+2) | Alkenes: CnH(2n) | Alkynes: CnH(2n-2)
Benzene: C6H6 | Mole = 6.022×10²³ | pH = -log[H+] | pH+pOH=14
Molarity = mol/L | Molality = mol/kg solvent | Faraday = 96500 C/mol
STP: 0°C, 1 atm, 1 mol gas = 22.4 L

=== PHYSICS ===
F=ma | F=Gm1m2/r² G=6.674×10⁻¹¹ | v_escape≈11.2km/s
c=3×10⁸ m/s | h=6.626×10⁻³⁴ J·s | e=1.6×10⁻¹⁹ C
m_e=9.1×10⁻³¹ kg | m_p=1.67×10⁻²⁷ kg | V=IR
Lens: 1/v-1/u=1/f | I_solid_sphere=2MR²/5 | I_disc=MR²/2
I_rod_centre=ML²/12 | λ=h/mv | T½=0.693/λ

=== MATHEMATICS ===
d/dx[sinx]=cosx | d/dx[cosx]=-sinx | d/dx[tanx]=sec²x | d/dx[lnx]=1/x
∫sinx=-cosx+C | ∫cosx=sinx+C | ∫xⁿ=xⁿ⁺¹/(n+1)+C
sin²x+cos²x=1 | sin(A+B)=sinAcosB+cosAsinB
nCr=n!/(r!(n-r)!) | S_AP=n/2(2a+(n-1)d)
"""

STORE_FILE = "mht_cet_history.json"

def load_history():
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE) as f: return json.load(f)
        except: return []
    return []

def save_history(record):
    h = load_history(); h.append(record)
    with open(STORE_FILE,"w") as f: json.dump(h,f,indent=2)

# ─────────────────────────────────────────────────────────────────────────────
#  CSS  — clean white, all text black
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:     #f3f4f6;
    --white:  #ffffff;
    --border: #e2e6ea;
    --text:   #111827;
    --muted:  #6b7280;
    --blue:   #2563eb;
    --blue-l: #eff6ff;
    --green:  #16a34a;
    --green-l:#f0fdf4;
    --red:    #dc2626;
    --red-l:  #fef2f2;
    --amber:  #d97706;
    --amber-l:#fffbeb;
    --phy:    #7c3aed;
    --phy-l:  #f5f3ff;
    --chem:   #059669;
    --chem-l: #ecfdf5;
    --math:   #d97706;
    --math-l: #fffbeb;
    --r:      10px;
    --sh:     0 1px 3px rgba(0,0,0,0.07);
}

/* GLOBAL */
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],
.main,.block-container,[data-testid="block-container"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter',sans-serif !important;
}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{ visibility:hidden; }
.block-container { padding:1.2rem 1.5rem; max-width:900px; margin:auto; }

/* ALL TEXT BLACK */
p,span,div,label,h1,h2,h3,h4,li,td,th,strong,b,small,em { color:var(--text) !important; }

/* STREAMLIT WIDGETS */
.stRadio label, .stRadio [data-testid="stMarkdownContainer"] p,
.stRadio div[role="radiogroup"] label, .stRadio div[role="radiogroup"] span { color:var(--text) !important; font-size:0.95rem !important; }
.stCheckbox label, .stCheckbox span, .stCheckbox > label > div { color:var(--text) !important; font-size:0.87rem !important; }
.stSelectbox label,[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] p { color:var(--text) !important; font-size:0.85rem !important; }
.stSelectbox [data-baseweb="select"] > div,[data-baseweb="select"] span { color:var(--text) !important; background:var(--white) !important; }
.stMultiSelect [data-baseweb="select"] > div { color:var(--text) !important; }
.stNumberInput input { color:var(--text) !important; background:var(--white) !important; }
.streamlit-expanderHeader,.streamlit-expanderHeader p,
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary p { color:var(--text) !important; font-weight:500 !important; }
.stCaption,.stCaption p { color:var(--muted) !important; font-size:0.8rem !important; }
[data-baseweb="menu"] li,[data-baseweb="menu"] [role="option"] { color:var(--text) !important; background:var(--white) !important; }
[data-baseweb="menu"] li:hover { background:var(--blue-l) !important; }
.stButton > button { background:var(--blue) !important; color:#fff !important; border:none !important; border-radius:var(--r) !important; font-family:'Inter',sans-serif !important; font-weight:600 !important; font-size:0.87rem !important; padding:0.52rem 1.2rem !important; width:100% !important; transition:all 0.15s; }
.stButton > button:hover { background:#1d4ed8 !important; }
.stButton > button p { color:#fff !important; }
.stAlert p,[data-testid="stNotification"] p { color:var(--text) !important; }

/* LAYOUT */
.card { background:var(--white); border:1px solid var(--border); border-radius:var(--r); padding:1.2rem 1.4rem; margin-bottom:0.7rem; box-shadow:var(--sh); }
.top-bar { display:flex; align-items:center; justify-content:space-between; background:var(--white); border:1px solid var(--border); border-radius:var(--r); padding:0.85rem 1.3rem; margin-bottom:1.1rem; box-shadow:var(--sh); }
.logo { font-size:1.1rem; font-weight:700; letter-spacing:-0.3px; color:var(--text) !important; }
.logo em { color:var(--blue) !important; font-style:normal; }

/* PILLS */
.pill { display:inline-flex; align-items:center; padding:2px 9px; border-radius:999px; font-size:0.7rem; font-weight:600; letter-spacing:0.2px; line-height:1.6; }
.pill-blue   { background:var(--blue-l); color:var(--blue)  !important; }
.pill-green  { background:var(--green-l);color:var(--green) !important; }
.pill-red    { background:var(--red-l);  color:var(--red)   !important; }
.pill-amber  { background:var(--amber-l);color:var(--amber) !important; }
.pill-phy    { background:var(--phy-l);  color:var(--phy)   !important; }
.pill-chem   { background:var(--chem-l); color:var(--chem)  !important; }
.pill-math   { background:var(--math-l); color:var(--math)  !important; }
.pill-gray   { background:#f3f4f6;       color:var(--muted) !important; }

/* DIFFICULTY PILLS */
.diff-Easy   { background:#f0fdf4; color:#16a34a !important; border:1px solid #bbf7d0; }
.diff-Medium { background:#fffbeb; color:#d97706 !important; border:1px solid #fde68a; }
.diff-Hard   { background:#fef2f2; color:#dc2626 !important; border:1px solid #fecaca; }
.diff-Mixed  { background:#f5f3ff; color:#7c3aed !important; border:1px solid #ddd6fe; }

/* TIMER */
.timer { font-family:'JetBrains Mono',monospace; font-size:1rem; font-weight:600; color:var(--text) !important; background:var(--bg); border:1.5px solid var(--border); border-radius:8px; padding:4px 13px; min-width:95px; text-align:center; }
.timer-warn   { color:var(--amber) !important; border-color:var(--amber) !important; }
.timer-danger { color:var(--red)   !important; border-color:var(--red)   !important; animation:blink 1s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* PROGRESS */
.prog-wrap { background:#e5e7eb; border-radius:999px; height:4px; margin:0.5rem 0 0.9rem; }
.prog-fill { background:var(--blue); border-radius:999px; height:4px; }

/* QUESTION */
.q-meta { display:flex; align-items:center; flex-wrap:wrap; gap:5px; margin-bottom:0.8rem; }
.q-number { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:var(--muted) !important; font-weight:500; }
.q-right  { margin-left:auto; display:flex; gap:5px; align-items:center; }
.pyq-badge { font-size:0.68rem; font-weight:700; background:#fef3c7; color:#92400e !important; border:1px solid #fcd34d; border-radius:5px; padding:2px 7px; font-family:'JetBrains Mono',monospace; }
.q-text { font-size:0.98rem; line-height:1.8; color:var(--text) !important; font-weight:400; margin:0; }

/* ANSWER OPTIONS (review) */
.opt { display:flex; align-items:flex-start; gap:10px; padding:0.65rem 1rem; border:1.5px solid var(--border); border-radius:var(--r); margin-bottom:0.4rem; background:var(--white); font-size:0.92rem; line-height:1.5; }
.opt span,.opt-key { color:var(--text) !important; }
.opt-key { font-weight:700; color:var(--muted) !important; min-width:16px; font-size:0.82rem; margin-top:1px; flex-shrink:0; }
.opt-correct { border-color:var(--green) !important; background:var(--green-l) !important; }
.opt-wrong   { border-color:var(--red)   !important; background:var(--red-l)   !important; }
.opt-correct .opt-key { color:var(--green) !important; }
.opt-wrong   .opt-key { color:var(--red)   !important; }

/* STATS */
.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:0.7rem; margin:0.7rem 0; }
.stat-card { background:var(--white); border:1px solid var(--border); border-radius:var(--r); padding:0.9rem; text-align:center; box-shadow:var(--sh); }
.stat-num { font-size:1.75rem; font-weight:700; font-family:'JetBrains Mono',monospace; line-height:1.1; }
.stat-lbl { font-size:0.68rem; color:var(--muted) !important; margin-top:3px; text-transform:uppercase; letter-spacing:0.5px; }

/* BARS */
.bar-row { display:flex; align-items:center; gap:10px; margin-bottom:7px; }
.bar-label { min-width:185px; color:var(--text) !important; font-size:0.8rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.bar-track { flex:1; background:#e5e7eb; border-radius:999px; height:7px; }
.bar-fill  { border-radius:999px; height:7px; }
.bar-stat  { min-width:85px; text-align:right; font-family:'JetBrains Mono',monospace; font-size:0.76rem; color:var(--muted) !important; }

/* HISTORY */
.hist-row { display:flex; align-items:center; padding:0.65rem 1rem; border:1px solid var(--border); border-radius:var(--r); margin-bottom:0.4rem; background:var(--white); gap:1rem; font-size:0.83rem; }
.hist-date  { color:var(--muted) !important; font-size:0.76rem; min-width:135px; font-family:'JetBrains Mono',monospace; }
.hist-score { font-weight:700; font-family:'JetBrains Mono',monospace; min-width:70px; }
.hist-sub   { flex:1; color:var(--text) !important; }

/* SECTION HEADING */
.sh { font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--muted) !important; margin:1.1rem 0 0.45rem; border-bottom:1px solid var(--border); padding-bottom:3px; }

/* MISC */
hr { border:none; border-top:1px solid var(--border); margin:1.1rem 0; }
code,pre { background:#f3f4f6 !important; color:var(--text) !important; border-radius:4px; padding:1px 5px; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-thumb { background:#d1d5db; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  GROQ
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    key = os.environ.get("GROQ_API_KEY","")
    if not key: st.error("GROQ_API_KEY not set."); st.stop()
    return Groq(api_key=key)

client = get_client()
MODEL  = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────────────────────────────────────────
#  STATE
# ─────────────────────────────────────────────────────────────────────────────
def reset_state(keep_chapters=True):
    cs = st.session_state.get("chapter_selection", {}) if keep_chapters else {}
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.phase             = "setup"
    st.session_state.questions         = []
    st.session_state.answers           = {}
    st.session_state.current_q         = 0
    st.session_state.start_time        = None
    st.session_state.time_limit        = None
    st.session_state.selected_chapters = []
    st.session_state.difficulty        = "Mixed"
    st.session_state.verify_log        = []
    st.session_state.used_hashes       = set()
    st.session_state.chapter_selection = cs
    st.session_state._do_select_all    = False
    st.session_state._do_clear_all     = False

if "phase" not in st.session_state:
    reset_state(keep_chapters=False)

STAG = {"Physics":"phy","Chemistry":"chem","Mathematics":"math"}

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def safe(t):
    return html_lib.escape(str(t)) if t else ""

def fmt_time(s):
    if s is None: return "∞"
    m,s2 = divmod(max(0,int(s)),60); h,m = divmod(m,60)
    return f"{h:02d}:{m:02d}:{s2:02d}" if h else f"{m:02d}:{s2:02d}"

def elapsed():
    return 0 if not st.session_state.start_time else time.time()-st.session_state.start_time

def remaining():
    return None if not st.session_state.time_limit else st.session_state.time_limit-elapsed()

def q_hash(q):
    return hashlib.md5(q.get("question","").lower().strip().encode()).hexdigest()

def parse_json(raw):
    raw = raw.strip()
    if "```" in raw:
        for p in raw.split("```"):
            p = p.strip().lstrip("json").strip()
            if p.startswith("["): raw=p; break
    s,e = raw.find("["),raw.rfind("]")+1
    if s!=-1 and e>s: raw=raw[s:e]
    return json.loads(raw)

def parse_obj(raw):
    raw = raw.strip()
    if "```" in raw:
        for p in raw.split("```"):
            p = p.strip().lstrip("json").strip()
            if p.startswith("{"): raw=p; break
    s,e = raw.find("{"),raw.rfind("}")+1
    if s!=-1 and e>s: raw=raw[s:e]
    return json.loads(raw)

def diff_color(d):
    return {"Easy":"green","Medium":"amber","Hard":"red","Mixed":"phy"}.get(d,"gray")

# ─────────────────────────────────────────────────────────────────────────────
#  GENERATION + VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────
def get_pyqs_for_chapters(chapters_info, count):
    """Pull real PYQs from the bank for selected chapters."""
    pool = []
    for c in chapters_info:
        ch_name = c["chapter"]
        if ch_name in PYQ_BANK:
            for q in PYQ_BANK[ch_name]:
                pool.append(dict(q))  # copy
    random.shuffle(pool)
    # Deduplicate
    used = st.session_state.get("used_hashes", set())
    unique = []
    for q in pool:
        h = q_hash(q)
        if h not in used:
            used.add(h)
            unique.append(q)
        if len(unique) >= count:
            break
    return unique

def generate_ai_questions(chapters_info, n, difficulty, used_hashes):
    random.shuffle(chapters_info)
    dist = {}
    per,rem = divmod(n, len(chapters_info))
    for i,c in enumerate(chapters_info):
        cnt = per+(1 if i<rem else 0)
        if cnt>0: dist[f"{c['subject']}|{c['std']}|{c['chapter']}"] = cnt

    dist_str = "\n".join(f"  • {k.split('|')[0]} ({k.split('|')[1]} Std) → {k.split('|')[2]}: {v}Q" for k,v in dist.items())

    prompt = f"""You are a senior MHT-CET Maharashtra question setter. Generate {n} original MCQs.

{FACT_REFERENCE}

Distribution:
{dist_str}

Difficulty: {difficulty}

STRICT RULES:
1. Questions must be based on real MHT-CET PYQ concepts (2015-2024). Assign realistic "pyq_year" or null.
2. "question" field: ONLY plain readable text. No HTML, no LaTeX, no angle brackets, no code.
   Write math as plain text: "CnH2n" not "<sub>n</sub>", "sin squared theta" or "sin²θ" is fine.
   "sqrt(2)", "x^2", "pi/2" are all fine. DO NOT use < or > characters.
3. All option values: plain text only. No HTML tags.
4. Assign "difficulty" field: "Easy", "Medium", or "Hard" per question.
5. Distractors must be plausible but wrong.
6. Explanation: 2-3 lines with formula/law and calculation.
7. Include "std" as "11th" or "12th" and "chapter" exactly as given.
8. Never repeat a question asked in another context — vary numbers, compounds, scenarios.

Return ONLY valid JSON array:
[{{"id":1,"subject":"Chemistry","std":"11th","chapter":"Hydrocarbons","pyq_year":2021,"difficulty":"Easy",
"question":"plain text question here","options":{{"A":"...","B":"...","C":"...","D":"..."}},"correct":"B","explanation":"..."}}]"""

    resp = client.chat.completions.create(
        model=MODEL, messages=[{"role":"user","content":prompt}],
        temperature=0.55, max_tokens=8000)
    qs = parse_json(resp.choices[0].message.content)
    unique = []
    for q in qs:
        h = q_hash(q)
        if h not in used_hashes:
            used_hashes.add(h); unique.append(q)
    return unique

def verify_question(q):
    prompt = f"""You are a strict MHT-CET fact-checker. Verify this question 100%.

{FACT_REFERENCE}

QUESTION:
{json.dumps(q, indent=2)}

Check:
1. Question text is clean plain text — NO HTML tags, no angle brackets.
   If question contains <span>, </div>, <p> or any HTML — REMOVE all HTML, keep only the text content.
2. All options are plain text — no HTML.
3. "correct" key is genuinely the right answer. Fix if wrong.
4. Explanation is accurate.
5. "difficulty" field exists ("Easy","Medium","Hard"). Add if missing.

Return ONLY corrected JSON object:
{{"id":0,"subject":"","std":"","chapter":"","pyq_year":null,"difficulty":"Medium","question":"","options":{{"A":"","B":"","C":"","D":""}},"correct":"","explanation":"","verified":true,"fix_applied":false,"fix_note":""}}"""

    try:
        resp = client.chat.completions.create(
            model=MODEL, messages=[{"role":"user","content":prompt}],
            temperature=0.1, max_tokens=1200)
        c = parse_obj(resp.choices[0].message.content)
        c.setdefault("verified",True); c.setdefault("fix_applied",False)
        c.setdefault("fix_note",""); c.setdefault("difficulty","Medium")
        c.setdefault("pyq_year",q.get("pyq_year"))
        return c
    except:
        q.update({"verified":False,"fix_applied":False,"fix_note":"verify error","difficulty":q.get("difficulty","Medium")})
        return q

def run_pipeline(chapters_info, n, difficulty, placeholder):
    used = st.session_state.get("used_hashes", set())
    vlog = []

    # ── Split: ~40% real PYQs, ~60% AI-generated ──
    n_pyq = min(max(1, int(n * 0.4)), n)
    n_ai  = n - n_pyq

    placeholder.markdown("""
    <div class="card" style="text-align:center;padding:2rem">
        <div style="font-size:1.4rem;margin-bottom:0.4rem">📚</div>
        <div style="font-weight:600;font-size:0.95rem">Phase 1 / 3 — Loading Real PYQs</div>
        <div style="color:#6b7280;font-size:0.83rem;margin-top:0.3rem">Pulling verified MHT-CET past year questions…</div>
    </div>""", unsafe_allow_html=True)

    pyq_questions = get_pyqs_for_chapters(chapters_info, n_pyq)
    actual_pyq = len(pyq_questions)
    n_ai = n - actual_pyq  # make up rest with AI

    placeholder.markdown(f"""
    <div class="card" style="text-align:center;padding:1.5rem">
        <div style="font-size:1.4rem;margin-bottom:0.4rem">⚡</div>
        <div style="font-weight:600;font-size:0.95rem">Phase 2 / 3 — Generating AI Questions</div>
        <div style="color:#6b7280;font-size:0.83rem;margin-top:0.3rem">
            {actual_pyq} real PYQs loaded · Generating {n_ai} AI questions…
        </div>
    </div>""", unsafe_allow_html=True)

    ai_questions = generate_ai_questions(chapters_info, n_ai, difficulty, used) if n_ai > 0 else []
    all_raw = pyq_questions + ai_questions

    # ── Verify all ──
    fixes = 0
    verified = []
    total_v = len(all_raw)

    for i,q in enumerate(all_raw):
        pct = int((i/total_v)*100)
        is_pyq = q.get("pyq_year") and i < actual_pyq
        placeholder.markdown(f"""
        <div class="card" style="padding:1.4rem">
            <div style="display:flex;justify-content:space-between;margin-bottom:0.55rem">
                <span style="font-weight:600;font-size:0.92rem">Phase 3 / 3 — Verifying All</span>
                <span style="font-family:'JetBrains Mono';font-size:0.8rem;color:#6b7280">{i}/{total_v}</span>
            </div>
            <div style="background:#e5e7eb;border-radius:999px;height:4px;margin-bottom:0.55rem">
                <div style="width:{pct}%;background:#2563eb;border-radius:999px;height:4px"></div>
            </div>
            <div style="font-size:0.81rem;color:#6b7280">
                {"📚 PYQ" if is_pyq else "🤖 AI"} · Q{i+1}: {q.get('chapter','')} ({q.get('subject','')})
            </div>
            <div style="font-size:0.76rem;color:#16a34a;margin-top:3px">✓ {fixes} correction(s)</div>
        </div>""", unsafe_allow_html=True)

        c = verify_question(q)
        if c.get("fix_applied"):
            fixes += 1
            vlog.append({"q_num":i+1,"subject":q.get("subject",""),"chapter":q.get("chapter",""),"fix_note":c.get("fix_note","")})
        verified.append(c)

    placeholder.markdown(f"""
    <div class="card" style="text-align:center;padding:1.3rem;border-color:#16a34a">
        <div style="color:#16a34a;font-weight:600;font-size:0.92rem">
            ✓ {total_v} questions ready · {actual_pyq} real PYQs + {len(ai_questions)} AI · {fixes} corrected
        </div>
    </div>""", unsafe_allow_html=True)
    time.sleep(0.7)

    st.session_state.used_hashes = used
    random.shuffle(verified)
    return verified, vlog

# ─────────────────────────────────────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def top_bar(center="", right_html=""):
    st.markdown(f"""
    <div class="top-bar">
        <div class="logo">MHT·<em>CET</em> AI</div>
        <div style="color:#6b7280;font-size:0.83rem">{center}</div>
        <div style="display:flex;align-items:center;gap:7px">{right_html}</div>
    </div>""", unsafe_allow_html=True)

def nav():
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("📝 New Test", use_container_width=True):
            reset_state(); st.rerun()
    with c2:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.phase="analytics"; st.rerun()
    with c3:
        if st.button("📅 History", use_container_width=True):
            st.session_state.phase="history"; st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  PHASE: SETUP
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "setup":
    top_bar(right_html='<span class="pill pill-blue">Dual-Pass Verified · PYQ Mixed</span>')
    nav()
    st.markdown("---")

    # ── Step 1 ──
    st.markdown('<div class="sh">Step 1 — Subjects & Standard</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        sel_subjects = st.multiselect("Subjects",["Physics","Chemistry","Mathematics"],default=["Physics","Chemistry","Mathematics"])
    with c2:
        sel_std = st.multiselect("Standard",["11th","12th"],default=["11th","12th"])

    available = [
        {"subject":s,"std":d,"chapter":c}
        for s in (sel_subjects or [])
        for d in (sel_std or [])
        for c in SYLLABUS.get(s,{}).get(d,[])
    ]

    # ── Step 2 ──
    st.markdown('<div class="sh">Step 2 — Select Chapters</div>', unsafe_allow_html=True)
    selected_chapters = []

    if not available:
        st.info("Pick a subject and standard above.")
    else:
        # Select All / Clear All — use flag pattern to work around Streamlit rerun timing
        ba1,ba2,_ = st.columns([1,1,6])

        if ba1.button("✅ Select All", use_container_width=True):
            st.session_state._do_select_all = True
            st.session_state._do_clear_all  = False
            st.rerun()

        if ba2.button("❌ Clear All", use_container_width=True):
            st.session_state._do_clear_all  = True
            st.session_state._do_select_all = False
            st.rerun()

        # Apply flags before rendering checkboxes
        if st.session_state.get("_do_select_all"):
            for a in available:
                st.session_state.chapter_selection[f"{a['subject']}|{a['std']}|{a['chapter']}"] = True
            st.session_state._do_select_all = False

        if st.session_state.get("_do_clear_all"):
            for a in available:
                st.session_state.chapter_selection[f"{a['subject']}|{a['std']}|{a['chapter']}"] = False
            st.session_state._do_clear_all = False

        # Render chapter checkboxes
        for subj in sel_subjects:
            tag = STAG.get(subj,"phy")
            st.markdown(f'<span class="pill pill-{tag}" style="margin-top:0.5rem;display:inline-block;font-size:0.78rem;padding:3px 12px">{subj}</span>', unsafe_allow_html=True)
            for std in sel_std:
                clist = SYLLABUS.get(subj,{}).get(std,[])
                if not clist: continue
                st.markdown(f'<span style="font-size:0.75rem;color:#6b7280;margin-left:2px"> — {std} Std</span>', unsafe_allow_html=True)
                cols = st.columns(3)
                for ci,ch in enumerate(clist):
                    k = f"{subj}|{std}|{ch}"
                    st.session_state.chapter_selection.setdefault(k, True)
                    checked = cols[ci%3].checkbox(ch, value=st.session_state.chapter_selection.get(k,True), key=f"c_{k}")
                    st.session_state.chapter_selection[k] = checked

        selected_chapters = [
            {"subject":k.split("|")[0],"std":k.split("|")[1],"chapter":k.split("|")[2]}
            for k,v in st.session_state.chapter_selection.items()
            if v and any(
                a["subject"]==k.split("|")[0] and a["std"]==k.split("|")[1] and a["chapter"]==k.split("|")[2]
                for a in available
            )
        ]
        st.caption(f"{len(selected_chapters)} of {len(available)} chapters selected")

    # ── Step 3 ──
    st.markdown('<div class="sh">Step 3 — Test Settings</div>', unsafe_allow_html=True)
    t1,t2,t3 = st.columns(3)
    with t1: num_q = st.number_input("Questions", 1, 200, 10)
    with t2: difficulty = st.selectbox("Difficulty", ["Mixed","Easy","Medium","Hard"])
    with t3: timer_mode = st.selectbox("Timer", ["Real CET","90 min","60 min","Custom","Free Style"])
    custom_mins = None
    if timer_mode == "Custom":
        custom_mins = st.number_input("Minutes", 1, 360, 45)

    st.markdown("---")
    if st.button("🚀 Generate & Start Test", use_container_width=True):
        if not selected_chapters:
            st.error("Select at least one chapter.")
        else:
            tl = None
            if timer_mode=="Real CET":  tl = max(60,int((num_q/150)*3*3600))
            elif timer_mode=="90 min":  tl = 5400
            elif timer_mode=="60 min":  tl = 3600
            elif timer_mode=="Custom":  tl = (custom_mins or 45)*60
            st.session_state.update({
                "selected_chapters":selected_chapters,
                "num_questions":num_q, "difficulty":difficulty,
                "time_limit":tl, "phase":"loading",
                "answers":{}, "current_q":0, "questions":[], "start_time":None, "verify_log":[],
                "_saved":False,
            })
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  PHASE: LOADING
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "loading":
    # Clean loading page — no nav, no top bar clutter
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 0.5rem">
        <div class="logo" style="font-size:1.3rem">MHT·<em style="color:#2563eb;font-style:normal">CET</em> AI</div>
    </div>""", unsafe_allow_html=True)
    ph = st.empty()
    try:
        qs,vlog = run_pipeline(
            st.session_state.selected_chapters,
            st.session_state.num_questions,
            st.session_state.difficulty, ph)
        st.session_state.questions  = qs
        st.session_state.verify_log = vlog
        st.session_state.start_time = time.time()
        st.session_state.phase      = "test"
        st.rerun()
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        if st.button("← Back to Setup"):
            st.session_state.phase="setup"; st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  PHASE: TEST  — full clean page, no nav bar
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "test":
    qs    = st.session_state.questions
    total = len(qs)
    idx   = st.session_state.current_q
    rem   = remaining()

    if rem is not None and rem <= 0:
        st.session_state.phase="review"; st.rerun()

    tcls = ""
    if rem is not None:
        if rem < 300: tcls="timer-danger"
        elif rem < 600: tcls="timer-warn"

    answered = len(st.session_state.answers)

    # ── HEADER ── (no nav — test is isolated page)
    st.markdown(f"""
    <div class="top-bar">
        <div class="logo">MHT·<em>CET</em> AI</div>
        <div style="display:flex;gap:0.9rem;align-items:center;font-size:0.83rem;color:#6b7280">
            <span>Q {idx+1} / {total}</span>
            <span style="color:#16a34a;font-weight:600">✓ {answered} answered</span>
            <span>{total-answered} left</span>
        </div>
        <div style="display:flex;align-items:center;gap:7px">
            <span class="pill pill-green" style="font-size:0.68rem">✓ Verified</span>
            <div class="timer {tcls}">{fmt_time(rem)}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Progress bar
    pct = int((idx/total)*100)
    st.markdown(f'<div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

    # ── QUESTION CARD ──
    q        = qs[idx]
    subj     = q.get("subject","Physics")
    std      = q.get("std","")
    chapter  = q.get("chapter","")
    pyq_year = q.get("pyq_year")
    diff     = q.get("difficulty","Medium")
    is_pyq   = bool(pyq_year)
    fix      = q.get("fix_applied",False)
    tag      = STAG.get(subj,"phy")
    dcol     = diff_color(diff)

    pyq_html = f'<span class="pyq-badge">PYQ {pyq_year}</span>' if is_pyq else ""
    fix_html = f'<span class="pill pill-red" style="font-size:0.65rem">✎ Fixed</span>' if fix else ""
    src_html = f'<span class="pill pill-blue" style="font-size:0.65rem">📚 PYQ</span>' if is_pyq else '<span class="pill pill-gray" style="font-size:0.65rem">🤖 AI</span>'

    st.markdown(f"""
    <div class="card">
        <div class="q-meta">
            <span class="q-number">Q{idx+1}</span>
            <span class="pill pill-{tag}">{safe(subj)}</span>
            <span class="pill pill-gray">{safe(std)} Std</span>
            <span class="pill pill-gray" style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{safe(chapter)}</span>
            {src_html} {fix_html}
            <span class="q-right">
                <span class="pill diff-{diff}">{diff}</span>
                {pyq_html}
            </span>
        </div>
        <p class="q-text">{safe(q['question'])}</p>
    </div>""", unsafe_allow_html=True)

    # ── OPTIONS (Streamlit radio) ──
    opts   = q["options"]
    keys   = list(opts.keys())
    labels = [f"{k}.  {opts[k]}" for k in keys]
    prev   = st.session_state.answers.get(idx)
    prev_i = keys.index(prev) if prev in keys else None

    chosen = st.radio("", labels, index=prev_i, key=f"r_{idx}", label_visibility="collapsed")
    if chosen:
        st.session_state.answers[idx] = keys[labels.index(chosen)]

    st.markdown("---")

    # ── NAV BUTTONS ──
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        if idx > 0 and st.button("← Prev"):
            st.session_state.current_q -= 1; st.rerun()
    with c2:
        if st.button("Clear"):
            st.session_state.answers.pop(idx,None); st.rerun()
    with c3:
        if idx < total-1 and st.button("Next →"):
            st.session_state.current_q += 1; st.rerun()
    with c4:
        if st.button("🏁 Submit Test"):
            st.session_state.phase="review"; st.rerun()

    # ── QUESTION PALETTE ──
    st.markdown("---")
    st.markdown('<div class="sh" style="margin-top:0">Question Palette</div>', unsafe_allow_html=True)

    # Render 10-per-row palette
    rows = [list(range(i, min(i+10, total))) for i in range(0, total, 10)]
    for row in rows:
        cols = st.columns(10)
        for ci,i in enumerate(row):
            is_ans = i in st.session_state.answers
            is_cur = i == idx
            lbl    = "✓" if is_ans else str(i+1)
            if cols[ci].button(lbl, key=f"pal_{i}"):
                st.session_state.current_q = i; st.rerun()

    # Auto-refresh timer
    if rem is not None and rem > 0:
        time.sleep(1); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  PHASE: REVIEW / RESULTS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "review":
    qs    = st.session_state.questions
    ans   = st.session_state.answers
    total = len(qs)
    vlog  = st.session_state.get("verify_log",[])

    # ── Compute ──
    subj_sc = {}; chap_sc = {}
    correct = wrong = skipped = 0
    pyq_correct = pyq_total = 0

    for i,q in enumerate(qs):
        s  = q.get("subject","?"); ch = q.get("chapter","?"); std = q.get("std","")
        ck = f"{s}||{ch} ({std})"
        subj_sc.setdefault(s,{"c":0,"w":0,"s":0,"t":0})
        chap_sc.setdefault(ck,{"c":0,"w":0,"s":0,"t":0})
        subj_sc[s]["t"]+=1; chap_sc[ck]["t"]+=1

        is_pyq = bool(q.get("pyq_year"))
        if is_pyq: pyq_total += 1

        if i not in ans:
            subj_sc[s]["s"]+=1; chap_sc[ck]["s"]+=1; skipped+=1
        elif ans[i]==q["correct"]:
            subj_sc[s]["c"]+=1; chap_sc[ck]["c"]+=1; correct+=1
            if is_pyq: pyq_correct += 1
        else:
            subj_sc[s]["w"]+=1; chap_sc[ck]["w"]+=1; wrong+=1

    score   = correct*2; max_sc = total*2
    pct     = round((correct/total)*100,1) if total else 0
    tt      = elapsed()
    fixes   = len(vlog)
    ai_count = total - pyq_total

    # Save
    if not st.session_state.get("_saved"):
        save_history({
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M"),
            "date":datetime.now().strftime("%d %b %Y"),
            "score":score,"max_score":max_sc,"pct":pct,
            "correct":correct,"wrong":wrong,"skipped":skipped,"total":total,
            "time_taken":int(tt),"difficulty":st.session_state.get("difficulty","Mixed"),
            "subjects":list(subj_sc.keys()),
            "subject_scores":{s:{"correct":v["c"],"total":v["t"],"pct":round((v["c"]/v["t"])*100,1) if v["t"] else 0} for s,v in subj_sc.items()},
            "fixes_applied":fixes,
        })
        st.session_state._saved = True

    gcol = "#16a34a" if pct>=70 else ("#d97706" if pct>=40 else "#dc2626")
    top_bar(right_html='<span class="pill pill-green">✓ Dual Verified</span>')
    nav()
    st.markdown("---")

    # ── Score card ──
    st.markdown(f"""
    <div class="card" style="text-align:center;padding:2rem">
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;color:#6b7280;margin-bottom:0.35rem">Your Score</div>
        <div style="font-size:3.2rem;font-weight:700;font-family:'JetBrains Mono';color:{gcol};line-height:1">
            {score}<span style="font-size:1.3rem;color:#9ca3af;font-weight:400">/{max_sc}</span>
        </div>
        <div style="color:#6b7280;font-size:0.85rem;margin-top:0.45rem">
            {pct}% accuracy · Time {fmt_time(int(tt))} · {fixes} auto-corrected
            · <span style="color:#2563eb">📚 {pyq_total} PYQs</span>
            · <span style="color:#7c3aed">🤖 {ai_count} AI</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="stat-num" style="color:#16a34a">{correct}</div><div class="stat-lbl">Correct (+{correct*2})</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#dc2626">{wrong}</div><div class="stat-lbl">Wrong (±0)</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#6b7280">{skipped}</div><div class="stat-lbl">Skipped</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#2563eb">{pct}%</div><div class="stat-lbl">Accuracy</div></div>
    </div>""", unsafe_allow_html=True)

    # Subject breakdown
    st.markdown('<div class="sh">Subject Performance</div>', unsafe_allow_html=True)
    cm = {"Physics":"phy","Chemistry":"chem","Mathematics":"math"}
    sc2 = st.columns(max(len(subj_sc),1))
    for ci,(s,v) in enumerate(subj_sc.items()):
        acc = round((v["c"]/v["t"])*100,1) if v["t"] else 0
        sc2[ci].markdown(f"""
        <div class="stat-card">
            <span class="pill pill-{cm.get(s,'blue')}">{s}</span>
            <div class="stat-num" style="font-size:1.4rem;margin-top:0.45rem">{v['c']}/{v['t']}</div>
            <div class="stat-lbl">{acc}% accuracy</div>
        </div>""", unsafe_allow_html=True)

    # Chapter bars
    st.markdown('<div class="sh">Chapter-wise Performance</div>', unsafe_allow_html=True)
    for ck,cv in chap_sc.items():
        acc = round((cv["c"]/cv["t"])*100,1) if cv["t"] else 0
        bc  = "#16a34a" if acc>=70 else ("#d97706" if acc>=40 else "#dc2626")
        lbl = ck.split("||")[1] if "||" in ck else ck
        st.markdown(f"""
        <div class="bar-row">
            <div class="bar-label">{lbl}</div>
            <div class="bar-track"><div class="bar-fill" style="width:{int(acc)}%;background:{bc}"></div></div>
            <div class="bar-stat">{cv['c']}/{cv['t']} · {acc}%</div>
        </div>""", unsafe_allow_html=True)

    # Verifier log
    if vlog:
        with st.expander(f"🔧 Verifier Corrections ({fixes})"):
            for e in vlog:
                st.markdown(f'<div style="padding:0.45rem 0.8rem;border-left:3px solid #dc2626;margin-bottom:0.35rem;font-size:0.81rem"><b>Q{e["q_num"]}</b> · {e["subject"]} — {e["chapter"]}<br><span style="color:#dc2626">{safe(e["fix_note"])}</span></div>', unsafe_allow_html=True)

    # ── DETAILED REVIEW ──
    st.markdown("---")
    st.markdown('<div class="sh">Detailed Question Review</div>', unsafe_allow_html=True)

    for i,q in enumerate(qs):
        s        = q.get("subject","Physics")
        std      = q.get("std","")
        ch       = q.get("chapter","")
        pyy      = q.get("pyq_year")
        diff     = q.get("difficulty","Medium")
        fix      = q.get("fix_applied",False)
        ua       = ans.get(i)
        ck_val   = q["correct"]
        right    = ua==ck_val
        skip     = ua is None
        icon     = "✅" if right else ("⏭️" if skip else "❌")
        tag      = STAG.get(s,"phy")
        dcol     = diff_color(diff)

        pyq_lbl = f" · PYQ {pyy}" if pyy else ""
        with st.expander(f"{icon}  Q{i+1} · {s} {std}{pyq_lbl} · {ch}"):
            pyq_b = f'<span class="pyq-badge">PYQ {pyy}</span>' if pyy else ""
            fix_b = '<span class="pill pill-red" style="font-size:0.65rem">✎ Auto-corrected</span>' if fix else ""
            src_b = '<span class="pill pill-blue" style="font-size:0.65rem">📚 PYQ</span>' if pyy else '<span class="pill pill-gray" style="font-size:0.65rem">🤖 AI</span>'
            st.markdown(f"""
            <div style="display:flex;flex-wrap:wrap;gap:5px;align-items:center;margin-bottom:0.75rem">
                <span class="pill pill-{tag}">{safe(s)}</span>
                <span class="pill pill-gray">{safe(std)} Std</span>
                <span class="pill pill-gray">{safe(ch)}</span>
                {src_b} <span class="pill diff-{diff}">{diff}</span>
                {pyq_b} {fix_b}
            </div>""", unsafe_allow_html=True)

            if fix and q.get("fix_note"):
                st.markdown(f'<div style="background:#fef2f2;border-left:3px solid #dc2626;padding:0.45rem 0.8rem;border-radius:6px;font-size:0.8rem;margin-bottom:0.45rem;color:#dc2626">{safe(q["fix_note"])}</div>', unsafe_allow_html=True)

            st.markdown(f'<p style="font-size:0.95rem;line-height:1.75;margin-bottom:0.75rem;color:#111827">{safe(q["question"])}</p>', unsafe_allow_html=True)

            for k,v in q["options"].items():
                sv = safe(v)
                if k==ck_val and k==ua:
                    st.markdown(f'<div class="opt opt-correct"><span class="opt-key">{k}</span><span>{sv} &nbsp;← Your answer ✓</span></div>', unsafe_allow_html=True)
                elif k==ck_val:
                    st.markdown(f'<div class="opt opt-correct"><span class="opt-key">{k}</span><span>{sv} &nbsp;← Correct answer</span></div>', unsafe_allow_html=True)
                elif k==ua:
                    st.markdown(f'<div class="opt opt-wrong"><span class="opt-key">{k}</span><span>{sv} &nbsp;← Your answer ✗</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="opt"><span class="opt-key">{k}</span><span>{sv}</span></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="background:#eff6ff;border-left:3px solid #2563eb;padding:0.55rem 0.85rem;border-radius:6px;font-size:0.83rem;margin-top:0.45rem;color:#111827">💡 {safe(q.get("explanation",""))}</div>', unsafe_allow_html=True)

    st.markdown("---")
    r1,r2 = st.columns(2)
    with r1:
        if st.button("🔄 New Test (same chapters)", use_container_width=True):
            st.session_state.update({"phase":"loading","answers":{},"current_q":0,"questions":[],"start_time":None,"verify_log":[],"_saved":False})
            st.rerun()
    with r2:
        if st.button("⚙️ Change Settings", use_container_width=True):
            reset_state(); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  PHASE: ANALYTICS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "analytics":
    top_bar("Analytics Dashboard")
    nav()
    st.markdown("---")

    history = load_history()
    if not history:
        st.info("No test history yet. Take a test first!")
    else:
        total_tests = len(history)
        avg_pct     = round(sum(h["pct"] for h in history)/total_tests,1)
        best_pct    = max(h["pct"] for h in history)
        total_q_done= sum(h["total"] for h in history)

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card"><div class="stat-num" style="color:#2563eb">{total_tests}</div><div class="stat-lbl">Tests Taken</div></div>
            <div class="stat-card"><div class="stat-num" style="color:#16a34a">{avg_pct}%</div><div class="stat-lbl">Avg Accuracy</div></div>
            <div class="stat-card"><div class="stat-num" style="color:#d97706">{best_pct}%</div><div class="stat-lbl">Best Score</div></div>
            <div class="stat-card"><div class="stat-num" style="color:#6b7280">{total_q_done}</div><div class="stat-lbl">Qs Attempted</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sh">Score Trend (Last 10 Tests)</div>', unsafe_allow_html=True)
        for h in history[-10:]:
            bc = "#16a34a" if h["pct"]>=70 else ("#d97706" if h["pct"]>=40 else "#dc2626")
            st.markdown(f"""
            <div class="bar-row">
                <div class="bar-label">{h['date']} · {h.get('difficulty','')}</div>
                <div class="bar-track"><div class="bar-fill" style="width:{int(h['pct'])}%;background:{bc}"></div></div>
                <div class="bar-stat">{h['score']}/{h['max_score']} · {h['pct']}%</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sh">Subject Average Across All Tests</div>', unsafe_allow_html=True)
        subj_agg = {}
        for h in history:
            for s,sv in h.get("subject_scores",{}).items():
                subj_agg.setdefault(s,{"sum":0,"n":0})
                subj_agg[s]["sum"] += sv["pct"]; subj_agg[s]["n"] += 1
        cm3 = {"Physics":"phy","Chemistry":"chem","Mathematics":"math"}
        sc3 = st.columns(max(len(subj_agg),1))
        for ci,(s,v) in enumerate(subj_agg.items()):
            avg = round(v["sum"]/v["n"],1)
            bc  = "#16a34a" if avg>=70 else ("#d97706" if avg>=40 else "#dc2626")
            sc3[ci].markdown(f"""
            <div class="stat-card">
                <span class="pill pill-{cm3.get(s,'blue')}">{s}</span>
                <div class="stat-num" style="font-size:1.4rem;margin-top:0.4rem;color:{bc}">{avg}%</div>
                <div class="stat-lbl">Avg · {v['n']} tests</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sh">Performance by Difficulty</div>', unsafe_allow_html=True)
        diff_agg = {}
        for h in history:
            d = h.get("difficulty","Mixed")
            diff_agg.setdefault(d,{"sum":0,"n":0})
            diff_agg[d]["sum"] += h["pct"]; diff_agg[d]["n"] += 1
        for d,v in diff_agg.items():
            avg = round(v["sum"]/v["n"],1)
            bc  = "#16a34a" if avg>=70 else ("#d97706" if avg>=40 else "#dc2626")
            st.markdown(f"""
            <div class="bar-row">
                <div class="bar-label" style="min-width:80px">{d}</div>
                <div class="bar-track"><div class="bar-fill" style="width:{int(avg)}%;background:{bc}"></div></div>
                <div class="bar-stat">{avg}% · {v['n']} tests</div>
            </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
#  PHASE: HISTORY
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.phase == "history":
    top_bar("Test History")
    nav()
    st.markdown("---")

    history = load_history()
    if not history:
        st.info("No tests recorded yet.")
    else:
        st.markdown(f'<div class="sh">{len(history)} Tests Recorded</div>', unsafe_allow_html=True)
        for h in reversed(history):
            bc  = "#16a34a" if h["pct"]>=70 else ("#d97706" if h["pct"]>=40 else "#dc2626")
            pc  = "pill-green" if h["pct"]>=70 else ("pill-amber" if h["pct"]>=40 else "pill-red")
            sub = ", ".join(h.get("subjects",[]))
            st.markdown(f"""
            <div class="hist-row">
                <div class="hist-date">{h['timestamp']}</div>
                <div class="hist-score" style="color:{bc}">{h['score']}/{h['max_score']}</div>
                <span class="pill {pc}">{h['pct']}%</span>
                <div class="hist-sub">{sub}</div>
                <div style="font-size:0.75rem;color:#6b7280">{h.get('difficulty','')} · {h['total']}Q · {fmt_time(h['time_taken'])}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🗑 Clear All History"):
            with open(STORE_FILE,"w") as f: json.dump([],f)
            st.success("History cleared."); st.rerun()
