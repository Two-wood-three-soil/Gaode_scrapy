import pandas as pd
import difflib
def string_similar(s1, s2):
    return difflib.SequenceMatcher(s1, s2).quick_ratio()

print(string_similar('aaa','bbb'))
