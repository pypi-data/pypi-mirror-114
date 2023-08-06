import re

def owoize(strings):
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
        for i in range(len(strings)):
            strings[i] = re.sub(key, patterns[key], strings[i])

    return strings