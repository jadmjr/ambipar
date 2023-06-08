import json

totalDamageTaken = 0
totalHitpointsHealed = 0
totalExperienceGained = 0
creatureKindsDamage = {"unknownOrigin": 0}
loot = {}
output = {
    "hitpointsHealed": 0,
    "damageTaken": {"total": 0, "byCreatureKind": {}},
    "experienceGained": 230,
    "loot": {},
}

# open the log file
file = open("tibia_log.txt", "r")

# line interator
for line in file:
    if "You lose" in line:
        totalDamageTaken += int(line.split()[3])
        try:
            creatureKindsDamage[
                line.split()[11].replace(".", "").replace("Black", "BlackKnight")
            ] += int(line.split()[3])
        except KeyError:
            creatureKindsDamage.update(
                {
                    line.split()[11]
                    .replace(".", "")
                    .replace("Black", "BlackKnight"): int(line.split()[3])
                }
            )
        except IndexError:
            creatureKindsDamage["unknownOrigin"] += int(line.split()[3])

    if "You healed" in line:
        totalHitpointsHealed += int(line.split()[5])

    if "You gained" in line:
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

#print("totalDamageTaken: " + str(totalDamageTaken))
#print("creatureKindsDamage: " + str(creatureKindsDamage))
#print("totalExperienceGained: " + str(totalExperienceGained))
#print("totalHitpointsHealed: " + str(totalHitpointsHealed))
#print("loot: " + str(loot))

output["hitpointsHealed"] = str(totalHitpointsHealed)   
output["damageTaken"]["total"] = str(totalDamageTaken) 
output["damageTaken"]["byCreatureKind"] = str(creatureKindsDamage)  
output["experienceGained"] = str(totalExperienceGained)  
output["loot"] = str(loot)  

#print("output: "+str(output))

with open('output.json', 'w') as outfile:
    json.dump(output, outfile)
