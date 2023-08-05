name = []
content = []

def setLang(lang):
    name = []
    content = []
    f = open("localization/" + lang + ".loc")
    for line in f:
        str = line.split(" = ")
        name.append(str[0])
        content.append(str[1])

def get(stringName):
    count = 0
    for n in name:
        if n == stringName:
            return content[count].rstrip()
        count += 1
    return "ERROR - Couldn't find " + stringName