import codecs
import re

outputFile = codecs.open("foodlist.txt", "w", "utf-8")
inputFile_List = open("F1.nq", "r+").read().splitlines()

regex = ur"label> \"\s?(.+?)\"? <"
for line in inputFile_List:
    value = re.findall(regex, line)

    if len(value) >= 1:
        print value[0]
        outputFile.write(u'%s\n' % (value[0]))
