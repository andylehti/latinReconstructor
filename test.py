from difflib import SequenceMatcher

def fuzzyMatch(s):
    s = s[-2:]
    s = s.translate(str.maketrans('znlwfvxkcdjt', 'smimeuumaaii'))
    d = {'1 0': ['ae'], '2 M': ['us', 'er'], '2 N': ['um'], '3 MF': ['is', 'es'], '3 N': ['e', 'al', 'ar'], '4 MF': ['us'], '4 N': ['u'], '5 0': ['es']}
    return max(d.keys(), key=lambda k: max(SequenceMatcher(None, s, v).ratio() for v in d[k]))

input_string = 'oz'
result = fuzzyMatch(input_string)
print(result)
