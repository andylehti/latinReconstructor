import unicodedata

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
        "AB": (f"by/with the {t}.", f"by/with the {p}."),
        "V": (f"Hey, {t}!", f"Hey, {p}!")
    }
    return tr

def normalize(t):
    return unicodedata.normalize('NFKD', t).encode('ASCII', 'ignore').decode()

def declension(t): 
    return t

s = {
    "1 0": {"N": ("a", "ae"), "G": ("ae", "ārum"), "D": ("ae", "īs"), "A": ("am", "ās"), "AB": ("ā", "īs"), "V": ("a", "ae")},
    "2 M": {"N": ("us", "ī"), "G": ("ī", "ōrum"), "D": ("ō", "īs"), "A": ("um", "ōs"), "AB": ("ō", "īs"), "V": ("e", "ī")},
    "2 N": {"N": ("um", "a"), "G": ("ī", "ōrum"), "D": ("ō", "īs"), "A": ("um", "a"), "AB": ("ō", "īs"), "V": ("um", "a")},
    "3 MF": {"N": ("", "ēs"), "G": ("is", "um"), "D": ("ī", "ibus"), "A": ("em", "ēs"), "AB": ("e", "ibus"), "V": ("", "ēs")},
    "3 N": {"N": ("", "a"), "G": ("is", "um"), "D": ("ī", "ibus"), "A": ("", "a"), "AB": ("e", "ibus"), "V": ("", "a")},
    "4 MF": {"N": ("us", "ūs"), "G": ("ūs", "uum"), "D": ("uī", "ibus"), "A": ("um", "ūs"), "AB": ("ū", "ibus"), "V": ("us", "ūs")},
    "4 N": {"N": ("ū", "ua"), "G": ("ūs", "uum"), "D": ("ū", "ibus"), "A": ("ū", "ua"), "AB": ("ū", "ibus"), "V": ("ū", "ua")},
    "5 0": {"N": ("ēs", "ēs"), "G": ("eī", "ērum"), "D": ("eī", "ēbus"), "A": ("em", "ēs"), "AB": ("ē", "ēbus"), "V": ("ēs", "ēs")}
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

word, translation = "Antōniopolis", "Cactus"
forms = process(word, translation)
for d, fm in forms.items(): 
    for c, (fm, tr) in fm.items(): 
        print(f"{d} {c}: {fm}, {normalize(fm)} \t {tr}")
