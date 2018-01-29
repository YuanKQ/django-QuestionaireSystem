# -*- coding: utf-8 -*-

import json
import codecs

def readFile():
    pass

infile = open("F:/code/java/KnowledgeMapping/data/try7.txt")#codecs.open("F:/code/java/KnowledgeMapping/data/try7.txt", "r", "utf-8") #F:/code/data/half-doctor.txt
# outfile = open("F:/code/data/try8.json", "w")#codecs.open("F:/code/data/try8.json", "w", "utf-8")

lcount = 1
qList = []
while 1:
    line = infile.readline()#.decode('UTF-8')
    if not line:
        break

    if lcount % 5 == 1:
        qDict={}
        qDict['id'] = lcount / 5
        qDict["qid"] = lcount / 5
        qDict['question_page'] = lcount / 100

    #handle the data in the form of json
    if lcount % 5 == 2:
        print line
        tempDict = eval(line)
        symList = list()
        if tempDict["data"].has_key("symptoms"):
            symList.extend(tempDict["data"]["symptoms"])
        if not tempDict["data"].has_key("slang_symptoms") and len(tempDict["data"]["slang_symtoms"]) != 0:
            symList.extend(tempDict["data"]["slang_symtoms"])

        if tempDict["data"].has_key("diseases"):
            symList.extend(tempDict["data"]["diseases"])
            # print tempDict["data"]["diseases"]
        if tempDict["data"].has_key("slang_diseases") and len(tempDict["data"]["slang_diseases"]) != 0:
            # print tempDict["data"]["slang_symtoms"]
            symList.extend(tempDict["data"]["slang_diseases"])
        qDict["choices"] = symList

    if lcount % 5 == 4:
        qDict['question_text'] = line#.encode("utf-8")

    if lcount % 5 == 0:
        print qDict
        qList.append(qDict)
        print "------------------------"

    lcount += 1

print qList

# outfile.write(json.dumps(qList))

infile.close()
# outfile.close()

