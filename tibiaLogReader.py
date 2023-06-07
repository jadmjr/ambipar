print("hello")

totalDamageTaken = 0
totalHitpointsHealed = 0
totalExperienceGained = 0
creatureKindsDamage = {"unknownOrigin": 0}
loot = {}
name = ''

#open the log file
file = open("tibia_log.txt", "r")

#line interator
for line in file:
  if("You lose" in line):
    totalDamageTaken+=int(line.split()[3])
    try:
        creatureKindsDamage[line.split()[11].replace(".","").replace("Black", "BlackKnight")] += int(line.split()[3])
    except KeyError:
        creatureKindsDamage.update({line.split()[11].replace(".","").replace("Black", "BlackKnight"): int(line.split()[3])})
    except IndexError:
         creatureKindsDamage["unknownOrigin"] += int(line.split()[3])

  if("You healed" in line):
    totalHitpointsHealed+=int(line.split()[5])

  if("You gained" in line):
    totalExperienceGained+=int(line.split()[3])

#[' a crossbow', ' 2 dragon ham', " a dragon's tail", ' 29 gold coins']
  if("Loot of" in line):
    objectsLine = line.split(":")[2].replace("\n", "").replace(".", "").split(",")          
    print(objectsLine)  

print("totalDamageTaken: "+str(totalDamageTaken))
print("creatureKindsDamage: "+str(creatureKindsDamage))
print("totalExperienceGained: "+str(totalExperienceGained))
print("totalHitpointsHealed: "+str(totalHitpointsHealed))


