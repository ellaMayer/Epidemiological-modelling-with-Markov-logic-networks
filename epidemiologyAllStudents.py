import os
import random
import csv


class IllStudent:
    def __init__(self, user, percent):
        self.user = user
        self.percent = percent


participants = ""
setParticipants = set()

with open('samples/coronaKiAll/participate.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        participants += f'{row[0]}, {row[1]}\n'
        user = row[1].replace(")", "")
        setParticipants.add(user)


infectedStudents = {}
for i in range(1, 18):
    infectedStudents[i] = list()

resistantStudents = {}
for i in range(1, 18):
    resistantStudents[i] = list()

setResistant = set()
setInfectious = set()
aktWeek = 1
evidenceRes = ""

for i in range(1, 18):
    entries = list()
    getFile = f'samples/coronaKiAll/output/Week{aktWeek}.txt'
    file = open(getFile, "r")
    setUsers = set()
    for line in file:
        str = f'{line}'
        str = str.replace("\"", " ")
        chunks = str.split('\t')
        userInfo = chunks[1].split()
        state = userInfo[0]
        state = state.replace("(", "")
        user = userInfo[1]
        percent = chunks[0]
        percent = float(percent.replace(",", "."))
        randomNum = random.random()
        newFile = f'samples/coronaKiAll/output/chosenOnes/Week{aktWeek}.txt'

        if randomNum <= percent:
            w = open(newFile, "a")
            w.write(f'{percent} infectious({user})\n')
            w.close()
            setUsers.add(user)
            setInfectious.add(user)
            if state == "infectious":
                if user not in resistantStudents[aktWeek]:
                    infectedStudents[aktWeek].append(IllStudent(user, percent))
                resistantStudents[aktWeek + 1].append(IllStudent(user, percent))
            if state == "resistant":
                resistantStudents[aktWeek].append(IllStudent(user, percent))

    evidenceInf = ""

    print(len(setResistant))
    if len(setParticipants) != 0:
        perRes = (len(setResistant) / len(setParticipants)) * 100

    for row in resistantStudents[aktWeek]:
        if row.user not in setResistant:
            evidenceRes += f'\nresistant({row.user})'
            setResistant.add(row.user)

    for row in infectedStudents[aktWeek]:
        if row.user not in setResistant:
            evidenceInf += f'\nisInfectious({row.user})'

    print(len(setUsers))
    print(len(setParticipants))

    perRes = 0
    perInf = 0

    if len(setParticipants) != 0:
        perInf = (len(setUsers) / len(setParticipants)) * 100

    log = ""
    w = open("samples/coronaKiAll/output/log.txt", "a")

    log += f'In Woche {aktWeek} sind {"%.2f" % perInf}% der Studenten infiziert und {"%.2f" % perRes}% der Studenten immun\n'
    w.write(log)
    w.close()

    w = open("samples/coronaKiAll/EVIDENCE.db", "a")
    w.write(participants)
    w.write(evidenceInf)
    w.write(evidenceRes)
    w.close()

    aktWeek += 1
    print("MATRGINAL-------------------------------------------------------------")
    commandLine = f'java -jar tuffy.jar -marginal -i samples/coronaKiAll/prog.mln -e samples/coronaKiAll/EVIDENCE.db ' \
        f'-queryFile samples/coronaKiAll/query.db -r samples/coronaKiAll/output/Week{aktWeek}.txt '
    os.system(commandLine)

    # print("MAP-------------------------------------------------------------------")
    # commandLine = f'java -jar tuffy.jar -i samples/coronaKiAll/prog.mln -e samples/coronaKiAll/EVIDENCE.db ' \
    #     f'-queryFile samples/coronaKiAll/query.db -r samples/coronaKiAll/outputMap/Week{aktWeek}.txt '
    # os.system(commandLine)

    os.remove("samples/coronaKiAll/EVIDENCE.db")

noInfUsers = ""
for entry in setParticipants:
    if entry not in setInfectious:
        noInfUsers += f'\n{entry} ist niemals infiziert!'

w = open("samples/coronaKiAll/output/log.txt", "a")
w.write(noInfUsers)
w.close()


