import streamlit as st
import unicodedata
import pandas as pd
from difflib import SequenceMatcher

st.title("Latin Declension Generator")

st.divider()

md = """
- Reconstructs Latin forms
- Generates all variants
- Provides precise English translations
- Produces all declensions
- Direct translations for machine learning
- Identifies likely declined forms
- Excludes forms for counterexample training
- Finds non-standard translations
"""

with st.popover("Features"):
    st.markdown(md)

def fuzzyMatch(s):
    s = s[-2:]
    s = s.translate(str.maketrans('znlwfvxkcdjt', 'smimeuumaaii'))
    d = {'1 0': ['ae'], '2 M': ['us', 'er'], '2 N': ['um'], '3 MF': ['is', 'es'], '3 N': ['e', 'al', 'ar'], '4 MF': ['us'], '4 N': ['u'], '5 0': ['es']}
    return max(d.keys(), key=lambda k: max(SequenceMatcher(None, s, v).ratio() for v in d[k]))

def getTR(t): 
    v = t[0] == 'a' or t[0] == "A"
    
    if t.endswith('y') and t[-2] not in 'aeiou': 
        p = t[:-1] + 'ies'
    elif t.endswith(('sh', 'ch', 'x', 'z')): 
        p = t + 'es'
    elif t.endswith('f'): 
        p = t[:-1] + 'ves'
    elif t.endswith('fe'): 
        p = t[:-2] + 'ves'
    elif t.endswith('o'): 
        p = t + 'es'
    elif t.endswith('us'): 
        p = t[:-2] + 'i'
    elif t.endswith('s'): 
        p = t + 'es'
    else: 
        p = t + 's'
    r = False if t.endswith('s') else True
    tr = {
        "N": (f"the {t} is.", f"the {p} are."),
        "G": (f"{t}'{'s' if r else ''}", f"{p}"),
        "D": (f"to/for the {t}", f"to/for the {p}"),
        "A": (f"{'an' if v else 'a'} {t}", f"the {p}"),
        "T": (f"by/with the {t}.", f"by/with the {p}."),
        "V": (f"Hey, {t}!", f"Hey, {p}!")
    }
    return tr

def normalize(t):
    return unicodedata.normalize('NFKD', t).encode('ASCII', 'ignore').decode()

def declension(t): 
    return t

s = {
    "1 0": {"N": ("a", "ae"), "G": ("ae", "ārum"), "D": ("ae", "īs"), "A": ("am", "ās"), "T": ("ā", "īs"), "V": ("a", "ae")},
    "2 M": {"N": ("us", "ī"), "G": ("ī", "ōrum"), "D": ("ō", "īs"), "A": ("um", "ōs"), "T": ("ō", "īs"), "V": ("e", "ī")},
    "2 N": {"N": ("um", "a"), "G": ("ī", "ōrum"), "D": ("ō", "īs"), "A": ("um", "a"), "T": ("ō", "īs"), "V": ("um", "a")},
    "3 MF": {"N": ("", "ēs"), "G": ("is", "um"), "D": ("ī", "ibus"), "A": ("em", "ēs"), "T": ("e", "ibus"), "V": ("", "ēs")},
    "3 N": {"N": ("", "a"), "G": ("is", "um"), "D": ("ī", "ibus"), "A": ("", "a"), "T": ("e", "ibus"), "V": ("", "a")},
    "4 MF": {"N": ("us", "ūs"), "G": ("ūs", "uum"), "D": ("uī", "ibus"), "A": ("um", "ūs"), "T": ("ū", "ibus"), "V": ("us", "ūs")},
    "4 N": {"N": ("ū", "ua"), "G": ("ūs", "uum"), "D": ("ū", "ibus"), "A": ("ū", "ua"), "T": ("ū", "ibus"), "V": ("ū", "ua")},
    "5 0": {"N": ("ēs", "ēs"), "G": ("eī", "ērum"), "D": ("eī", "ēbus"), "A": ("em", "ēs"), "T": ("ē", "ēbus"), "V": ("ēs", "ēs")}
}

def process(word, t): 
    word = declension(word)
    tr = getTR(t)
    f = {}
    st = {
        "1 0": word[:-1], "2 M": word[:-2], "2 N": word[:-2], 
        "3 MF": word[:-1], "3 N": word[:-1], 
        "4 MF": word[:-2], "4 N": word[:-1], "5 0": word[:-2]
    }
    for d, endings in s.items(): 
        f[d] = {f"{c} {n}": (st[d] + suff, tr[c][0] if n == "S" else tr[c][1]) for c, (sufS, sufP) in endings.items() for n, suff in [("S", sufS), ("P", sufP)]}
    
    return f

def mapDeclension(d):
    declension_map = {
        "1 0": "1st Declension",
        "2 M": "2nd Declension",
        "2 N": "2nd Declension",
        "3 MF": "3rd Declension",
        "3 N": "3rd Declension",
        "4 MF": "4th Declension",
        "4 N": "4th Declension",
        "5 0": "5th Declension"
    }
    return declension_map[d]

def mapGender(d):
    gender_map = {
        "1 0": "Feminine",
        "2 M": "Masculine",
        "2 N": "Neuter",
        "3 MF": "Masculine/Feminine",
        "3 N": "Neuter",
        "4 MF": "Masculine/Feminine",
        "4 N": "Neuter",
        "5 0": "Feminine"
    }
    return gender_map[d]

def mapCase(c):
    case_map = {
        "N S": "Nominative",
        "N P": "Nominative",
        "G S": "Genitive",
        "G P": "Genitive",
        "D S": "Dative",
        "D P": "Dative",
        "A S": "Accusative",
        "A P": "Accusative",
        "T S": "Ablative",
        "T P": "Ablative",
        "V S": "Vocative",
        "V P": "Vocative"
    }
    return case_map[c]

def mapNumber(c):
    return "s." if "S" in c else "pl."

col1, col2 = st.columns(2)

with col1:
    word = st.text_input("", placeholder="Latin Word")

with col2:
    translation = st.text_input("", placeholder="English Translation")

if st.button("Process"):
    forms = process(word, translation)
    r = fuzzyMatch(normalize(word))
    data = []
    for d, fm in forms.items(): 
        for c, (fm, tr) in fm.items():
            e = "V" if r == d else ""
            icon = "✅" if e == "V" else ""
            case = mapCase(c)
            number = mapNumber(c)
            data.append([icon, mapDeclension(d), mapGender(d), case, fm, normalize(fm), tr, number])
    
    df = pd.DataFrame(data, columns=["", "Declension", "Gender", "Case", "Form", "Normalized Form", "Translation", "Plurality"])
    st.dataframe(df.style.set_properties(**{'text-align': 'left'}))

    # Export to CSV
    csv = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name=f'{word}.csv', mime='text/csv')
