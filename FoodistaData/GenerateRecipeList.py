import codecs
import re

outputFile = codecs.open("recipelist.txt", "w", "utf-8")
inputFile_List = open("F2.nq", "r+").read().splitlines()

regex = ur"title> \"\s?(.+?)\"? <"
for line in inputFile_List:
    value = re.findall(regex, line)

    if len(value) >= 1:
        print value[0]
        outputFile.write(u'%s\n' % (value[0]))
