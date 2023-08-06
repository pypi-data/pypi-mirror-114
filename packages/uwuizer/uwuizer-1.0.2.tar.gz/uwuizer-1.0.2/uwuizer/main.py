import re

def owoize(string):
    #Note that order is important in these as they are executed in order
    patterns = {
        r"\?$" : "Ouuh~wOuuh~♪",
        r"\?" : "?~~~",
        r"l" : "w",
        r"please" : "pws",
        r"Please" : "~Pws",
        r"r" : "w",
        r"\!" : "^w^",
        r"ary" : "aryweary"
        }

    for key in patterns:
        regex = re.compile(key)
        string = re.sub(key, patterns[key], string)

    return string