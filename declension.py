import unicodedata
from difflib import SequenceMatcher

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

word, translation = "Antōniopolis", "Cactus"
forms = process(word, translation)
r = fuzzyMatch(normalize(word))

for d, fm in forms.items(): 
    for c, (fm, tr) in fm.items():
        e = "V" if r == d else "O"
        print(f"{e} {d[0]} {c}: {fm}, {normalize(fm)} \t {tr}")