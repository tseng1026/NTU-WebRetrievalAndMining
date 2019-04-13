# python 3
import os
import xml.etree.ElementTree as ET

def ParseVocb(Dir):
	### Format: vocb = [vocb, ...]
	read = open(Dir + "vocab.all", "r")
	vocb = read.read().split("\n")

	print("[Done] Parsing \"vocab.all\"!")
	return list(vocb)[:-1]


def ParseFile(Dir, Doc):
	### Format: file = [(file, size), ...]
	read = open(Dir + "file-list", "r")
	
	avdl = 0
	file = []
	for item in read.readlines():
		size = os.path.getsize(Doc + item[8:-1])
		avdl += size

		file.append((item[16:-1].lower(), size))
		
	print("[Done] Parsing \"file-list\"!")
	return file, avdl / len(file)


def ParseInvt(Dir):
	### Format: invt = {(word[0], word[1]): [fileNumb, (fileIndex, fileTime), ...], ...}
	read = open(Dir + "inverted-file", "r")

	temp = ""
	invt = {}
	for item in read.readlines():
		word = item.split(" ")
		word = [int(n) for n in word]
		
		if len(word) == 3:
			temp = (word[0], word[1])
			invt[temp] = [word[2]]

		if len(word) == 2:
			invt[temp].append((word[0], word[1]))

	print("[Done] Parsing \"inverted-file\"!")
	return invt


def ParseQury(Dir):
	### Format: qury = [[number, title, question, narrative, concept], ...]
	tree = ET.ElementTree(file = Dir)
	root = tree.getroot()
	
	temp = 0
	qury = []
	for item in root:
		qury.append([])
		qury[temp].append(item[0].text.strip()[14:])
		qury[temp].append(item[1].text.strip())
		qury[temp].append(item[2].text.strip()[:-1])
		qury[temp].append(item[3].text.strip().split(u'。')[0])
		qury[temp].append(item[4].text.strip()[:-1])
		temp += 1

	print("[Done] Parsing \"query-test.xml\"!")
	return qury