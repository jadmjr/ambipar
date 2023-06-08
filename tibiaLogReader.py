import json

totalDamageTaken = 0
totalHitpointsHealed = 0
totalExperienceGained = 0
unknownOriginDamage = 0
damageCreatureKind = {}
blackKnightGains = 0
blackKnightLoses = 0
blackKnightHealth = 0

loot = {}
output = {
    "hitpointsHealed": 0,
    "damageTaken": {"total": 0,"unknownOriginDamage":0 , "byCreatureKind": {}},
    "experienceGained": 0,
    "loot": {},
    "blackKnightHealth":0
}

# open the log file
file = open("tibia_log.txt", "r")

# line interator
for line in file:
    if "You lose" in line:
        totalDamageTaken += int(line.split()[3])
        pos = int(line.rfind("by a"))
        if(pos>-1):        
            creatureKind = line[pos+5:].replace(" ","").replace(".","").replace("\n","")  
            try:
                damageCreatureKind[creatureKind] += int(line.split()[3])
            except KeyError:
                damageCreatureKind.update(
                {
                    creatureKind: int(line.split()[3])
                }
            )
            #except IndexError:
             #   unknownOriginDamage += int(line.split()[3])
            if("Black Knight" in line):
                blackKnightGains+=int(line.split()[3])
        else:
            unknownOriginDamage += int(line.split()[3])   
    if "A Black Knight loses" in line:
        blackKnightLoses+=int(line.split()[5])

    if "You healed" in line:
        totalHitpointsHealed += int(line.split()[5])

    if ("You gained" in line and "experience" in line):
        totalExperienceGained += int(line.split()[3])

    if "Loot of" in line and "nothing." not in line:
        objectsLine = line.split(":")[2]
        objectsLine = (
            objectsLine[1:]
            .replace(".", "")
            .replace("\n", "")
            .replace(", ", ",")
            .replace("'s", "")
            .split(",")
        )

        for x in objectsLine:
            arrayObjectLine = x.split()
            arrayObjectLineLength = len(arrayObjectLine)

            if arrayObjectLineLength == 1:
                name = arrayObjectLine[0]
                value = 1
            elif arrayObjectLineLength == 2:
                if arrayObjectLine[0] == "a":
                    value = 1
                    name = arrayObjectLine[1]
                else:
                    try:
                        value = int(arrayObjectLine[0])
                        name = arrayObjectLine[1]
                    except:
                        value = 1
                        name = arrayObjectLine[0] + arrayObjectLine[1]
            elif arrayObjectLineLength == 3:
                if arrayObjectLine[0] == "a":
                    value = 1
                    name = arrayObjectLine[1] + arrayObjectLine[2]
                else:
                    try:
                        value = int(arrayObjectLine[0])
                        name = arrayObjectLine[1] + arrayObjectLine[2]
                    except:
                        value = 1
                        name = (
                            arrayObjectLine[0] + arrayObjectLine[1] + arrayObjectLine[2]
                        )
                    name = name.replace("goldcoins", "goldcoin")
            elif arrayObjectLineLength == 4:
                if arrayObjectLine[0] == "a":
                    value = 1
                    name = arrayObjectLine[1] + arrayObjectLine[2] + arrayObjectLine[3]
                else:
                    try:
                        value = int(arrayObjectLine[0])
                        name = (
                            arrayObjectLine[1] + arrayObjectLine[2] + arrayObjectLine[3]
                        )
                    except:
                        value = 1
                        name = (
                            arrayObjectLine[0]
                            + arrayObjectLine[1]
                            + arrayObjectLine[2]
                            + arrayObjectLine[3]
                        )
                    name = name.replace("goldcoins", "goldcoin")
            try:
                loot[name] += value
            except KeyError:
                loot.update({name: value})
            name = ""
            value = 0

blackKnightHealth = blackKnightGains - blackKnightLoses

output["hitpointsHealed"] = totalHitpointsHealed
output["damageTaken"]["total"] = totalDamageTaken
output["damageTaken"]["unknownOriginDamage"] = unknownOriginDamage
output["damageTaken"]["byCreatureKind"] = damageCreatureKind
output["experienceGained"] = totalExperienceGained  
output["loot"] = loot
output["blackKnightHealth"] = blackKnightHealth

with open('output.json', 'w') as outfile:
    json.dump(output, outfile)

